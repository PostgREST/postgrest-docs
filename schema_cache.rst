.. _schema_cache:

Schema Cache
============

Users are often confused by PostgREST's database schema cache. It is present because detecting foreign key relationships between tables (including how those relationships pass through views) is necessary, but costly. API requests consult the schema cache as part of :ref:`resource_embedding`. However if the schema changes while the server is running it results in a stale cache and leads to errors claiming that no relations are detected between tables.

.. important::

   Since v5.0, PostgREST also makes use of the schema cache for stored functions metadata: parameters, return type, volatility.
   It also uses the schema cache for resolving overloaded functions. You should refresh the cache if a change in any of the prior is done.

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