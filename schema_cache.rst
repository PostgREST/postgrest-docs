.. _schema_cache:

Schema Cache
============

Certain PostgREST features need information from the database schema; however, accessing the database directly would be too costly, that is why PostgREST generates a database schema cache on startup and gets the information from it instead:

+--------------------------------------------+-------------------------------------------------------------------------------+
| Feature                                    | Required Metadata                                                             |
+============================================+===============================================================================+
| :ref:`resource_embedding`                  | Foreign key constraints (to determine relationships between tables)           |
+--------------------------------------------+-------------------------------------------------------------------------------+
| :ref:`Database Functions <s_procs>`        | Function's metadata (parameters, return type, volatility and                  |
|                                            | `overloading <https://www.postgresql.org/docs/current/xfunc-overload.html>`_) |
+--------------------------------------------+-------------------------------------------------------------------------------+
| :ref:`Upserts <upsert>`                    | Primary keys                                                                  |
+--------------------------------------------+-------------------------------------------------------------------------------+
| :ref:`insert_update`                       | Primary keys (in order to return the Location header)                         |
+--------------------------------------------+-------------------------------------------------------------------------------+
| :ref:`OPTIONS requests <options_requests>` | View primary key columns and INSTEAD OF TRIGGERS                              |
+--------------------------------------------+-------------------------------------------------------------------------------+
| :ref:`open-api`                            | Table columns, primary keys and foreign keys                                  |
+                                            +-------------------------------------------------------------------------------+
|                                            | View columns and INSTEAD OF TRIGGERS                                          |
+                                            +-------------------------------------------------------------------------------+
|                                            | Function's metadata                                                           |
+--------------------------------------------+-------------------------------------------------------------------------------+

The Stale Schema Cache
----------------------

When you make changes on the metadata mentioned above while PostgREST is running, the schema cache turns stale. Future requests you make related to these changes will need the :ref:`schema to be reloaded <schema_reloading>`; otherwise, you'll get an error instead of the expected result.

For instance, let's see what would happen if you have a stale schema for foreign key relationships and function metadata:

Stale Foreign Key Relationships
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Suppose you add a ``cities`` table to your database. This table has a foreign key ``country_id`` referencing an existing ``countries`` table. Then, you make a request to get the data from ``cities`` and their ``countries``:

.. code-block:: http

  GET /cities?select=name,country:countries(id,name) HTTP/1.1

But instead, you get an error message that looks like this:

.. code-block:: json

  {
    "hint": "If a new foreign key between these entities was created in the database, try reloading the schema cache.",
    "message": "Could not find a relationship between cities and countries in the schema cache"
  }

As you can see, PostgREST couldn't find the relationship in the schema cache. See the section :ref:`schema_reloading` to solve this issue.

Stale Function Metadata
~~~~~~~~~~~~~~~~~~~~~~~

Suppose you create this function on the database while PostgREST is running:

.. code-block:: plpgsql

  CREATE FUNCTION plus_one(num integer)
  RETURNS integer AS $$
   SELECT num + 1;
  $$ LANGUAGE SQL IMMUTABLE;

Then, you make this request:

.. code-block:: http

  GET /rpc/plus_one?num=1 HTTP/1.1

On a stale schema, PostgREST will assume :code:`text` as the default type for the function argument ``num``. Thus, the response you get is:

.. code-block:: json

 {
  "hint":"No function matches the given name and argument types. You might need to add explicit type casts.",
  "details":null,
  "code":"42883",
  "message":"function test.plus_one(num => text) does not exist"
 }

See the section :ref:`schema_reloading` to solve this issue.

.. _schema_reloading:

Schema Reloading
----------------

To refresh the cache without restarting the PostgREST server, send the server process a SIGUSR1 signal:

.. code:: bash

  killall -SIGUSR1 postgrest

.. note::

   To refresh the cache in docker:

   .. code:: bash

     docker kill -s SIGUSR1 <container>

     # or in docker-compose
     docker-compose kill -s SIGUSR1 <service>

The above is the manual way to do it. To automate the schema reloads, use a database trigger like this:

.. code-block:: postgresql

  CREATE OR REPLACE FUNCTION public.notify_ddl_postgrest()
    RETURNS event_trigger
   LANGUAGE plpgsql
    AS $$
  BEGIN
    NOTIFY ddl_command_end;
  END;
  $$;

  CREATE EVENT TRIGGER ddl_postgrest ON ddl_command_end
     EXECUTE PROCEDURE public.notify_ddl_postgrest();

Then run the `pg_listen <https://github.com/begriffs/pg_listen>`_ utility to monitor for that event and send a SIGUSR1 when it occurs:

.. code-block:: bash

  pg_listen <db-uri> ddl_command_end $(which killall) -SIGUSR1 postgrest

Now, whenever the structure of the database schema changes, PostgreSQL will notify the ``ddl_command_end`` channel, which will cause ``pg_listen`` to send PostgREST the signal to reload its cache. Note that pg_listen requires full path to the executable in the example above.
