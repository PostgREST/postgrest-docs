.. _schema_cache:

Schema Cache
============

PostgREST caches metadata from the database schema to avoid repeating expensive queries. This metadata is not required by all of the PostgREST features, only the following:

+--------------------------------------------+-------------------------------------------------------------------------------+
| Feature                                    | Required Metadata                                                             |
+============================================+===============================================================================+
| :ref:`resource_embedding`                  | Foreign key constraints                                                       |
+--------------------------------------------+-------------------------------------------------------------------------------+
| :ref:`Stored Functions <s_procs>`          | Function signature (parameters, return type, volatility and                   |
|                                            | `overloading <https://www.postgresql.org/docs/current/xfunc-overload.html>`_) |
+--------------------------------------------+-------------------------------------------------------------------------------+
| :ref:`Upserts <upsert>`                    | Primary keys                                                                  |
+--------------------------------------------+-------------------------------------------------------------------------------+
| :ref:`Insertions <insert_update>`          | Primary keys (optional: only if the Location header is requested)             |
+--------------------------------------------+-------------------------------------------------------------------------------+
| :ref:`OPTIONS requests <options_requests>` | View INSTEAD OF TRIGGERS and primary keys                                     |
+--------------------------------------------+-------------------------------------------------------------------------------+
| :ref:`open-api`                            | Table columns, primary keys and foreign keys                                  |
+                                            +-------------------------------------------------------------------------------+
|                                            | View columns and INSTEAD OF TRIGGERS                                          |
+                                            +-------------------------------------------------------------------------------+
|                                            | Function signature                                                            |
+--------------------------------------------+-------------------------------------------------------------------------------+

The Stale Schema Cache
----------------------

When you make changes on the metadata mentioned above, the schema cache will turn stale on a running PostgREST. Future requests that use the above features will need the :ref:`schema cache to be reloaded <schema_reloading>`; otherwise, you'll get an error instead of the expected result.

For instance, let's see what would happen if you have a stale schema for foreign key relationships and function signature:

Stale Foreign Key Relationships
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Suppose you add a ``cities`` table to your database. This table has a foreign key referencing an existing ``countries`` table. Then, you make a request to get the ``cities`` and their belonging ``countries``:

.. code-block:: http

  GET /cities?select=name,country:countries(id,name) HTTP/1.1

But instead, you get an error message that looks like this:

.. code-block:: json

  {
    "hint": "If a new foreign key between these entities was created in the database, try reloading the schema cache.",
    "message": "Could not find a relationship between cities and countries in the schema cache"
  }

As you can see, PostgREST couldn't find the newly created foreign key in the schema cache. See the section :ref:`schema_reloading` to solve this issue.

Stale Function Signature
~~~~~~~~~~~~~~~~~~~~~~~~

Suppose you create the following function while PostgREST is running:

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

Schema Cache Reloading
----------------------

To refresh the cache without restarting the PostgREST server, send the server process a SIGUSR1 signal:

.. code:: bash

  killall -SIGUSR1 postgrest

.. note::

   To refresh the cache in docker:

   .. code:: bash

     docker kill -s SIGUSR1 <container>

     # or in docker-compose
     docker-compose kill -s SIGUSR1 <service>

Another option is to send a `database notification event <https://www.postgresql.org/docs/current/sql-notify.html>`_ from any PostgreSQL client by executing the ``NOTIFY`` command as follows:

.. code-block:: postgresql

  NOTIFY pgrst

  -- Works the same way as:

  NOTIFY pgrst, 'reload schema'

.. important::

  The ``db-channel-enable`` :ref:`configuration parameter <db-channel-enabled>` enables the notification channel by default.
  This setting is incompatible with connection poolers like PgBouncer in transaction pooling mode. Set it to ``false`` if you are using PostgREST behind a connection pooler.

If the notification event is set to fire on a database event trigger, then **automatic schema cache reloading** is possible. For example:

.. code-block:: postgresql

  -- Create an event trigger function
  CREATE OR REPLACE FUNCTION public.pgrst_watch() RETURNS event_trigger
    LANGUAGE plpgsql
    AS $$
  BEGIN
    NOTIFY pgrst;
  END;
  $$;

  -- This event trigger will fire after every ddl_command_end event
  -- See https://www.postgresql.org/docs/current/event-trigger-definition.html
  CREATE EVENT TRIGGER pgrst_watch
    ON ddl_command_end
    EXECUTE PROCEDURE pgrst_watch();

Now, whenever the ``pgrst_watch`` trigger is fired in the database, PostgREST will automatically reload the schema cache.

To disable auto reloading, drop the trigger:

.. code-block:: postgresql

  DROP EVENT TRIGGER pgrst_watch