.. _schema_cache:

Schema Cache
============

PostgREST uses the database schema cache to get information for several of its features:

- For :ref:`resource_embedding`, it needs relationships' information, such as related tables, foreign keys, cardinalities, etc.
- For :ref:`s_procs`, it needs access to their metadata, for example, parameters, return type or volatility. It also needs to verify if the function is overloaded.
- To do an :ref:`upsert`, it looks for the primary keys.
- To do an INSERT, it also looks for the primary keys in order to return the Location header.
- For OPTION requests, it verifies the existence and the data modification capabilities of a table or view.
- For :ref:`open-api`, it needs information about objects in the database (e.g., object description, columns and parameters).

Retrieving this information directly from the database is costly, that is why PostgREST uses a database schema cache instead. When you change any of the information mentioned above while PostgREST is running, the schema cache turns stale. You then need to reload the schema before you make a request related to these changes, otherwise you'll receive an error instead of the expected response.

For instance, suppose you add a ``cities`` table to your database. This table has a foreign key ``country_id`` referencing an existing ``countries`` table. Then, you make a request to get the data from ``cities`` and their ``countries``:

.. code-block:: http

  GET /cities?select=name,country:countries(id,name) HTTP/1.1

But instead, you get an error message that looks like this:

.. code-block:: json

  {
    "hint": "If a new foreign key between these entities was created in the database, try reloading the schema cache.",
    "message": "Could not find a relationship between cities and countries in the schema cache"
  }

As you can see PostgREST couldn't find the relationship in the schema cache. To solve this you only need to reload the schema and repeat the request.

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