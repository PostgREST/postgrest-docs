.. _tut0:

Tutorial 0 - Get it Running
===========================

Welcome to PostgREST! In this pre-tutorial we're going to get things running so you can create your first simple API.

PostgREST is a standalone web server which turns a PostgreSQL database into a RESTful API. It serves an API that is customized based on the structure of the underlying database.

.. image:: ../_static/tuts/tut0-request-flow.png

To make an API we'll simply be building a database. All the endpoints and permissions come from database objects like tables, views, roles, and stored procedures. These tutorials will cover a number of common scenarios and how to model them in the database.

By the end of this tutorial you'll have a working database, PostgREST server, and a simple single-user todo list API.

Step 1. Relax, we'll help
-------------------------

As you begin the tutorial, pop open the project `chat room <https://gitter.im/begriffs/postgrest>`_ in another tab.  There are a nice group of people active in the project and we'll help you out if you get stuck.

Step 2. Install PostgreSQL
--------------------------

You'll need a modern copy of the database running on your system, either natively or in a Docker instance. We require PostgreSQL 9.3 or greater, but recommend at least 9.5 for row-level security features that we'll use in future tutorials.

If you're already familiar with using PostgreSQL and have it installed on your system you can use the existing installation. For this tutorial we'll describe how to use the database in Docker because database configuration is otherwise too complicated for a simple tutorial.

If Docker is not installed, you can get it `here <https://www.docker.com/community-edition#download>`_. Next, let's pull and start the database image:

.. code-block:: bash

  sudo docker run --name tutorial -p 5432:5432 \
                  -e POSTGRES_PASSWORD=mysecretpassword \
                  -d postgres

This will run the Docker instance as a daemon and expose port 5432 to the host system so that it looks like an ordinary PostgreSQL server to the rest of the system.

Step 3. Install PostgREST
-------------------------

PostgREST is distributed as a single binary, with versions compiled for major distributions of Linux/BSD/Windows. Visit the `latest release <https://github.com/begriffs/postgrest/releases/latest>`_ for a list of downloads. In the event that your platform is not among those already pre-built, see :ref:`build_source` for instructions how to build it yourself. Also let us know to add your platform in the next release.

The pre-built binaries for download are :code:`.tar.xz` compressed files (except Windows which is a zip file). To extract the binary, go into the terminal and run

.. code-block:: bash

  # download from https://github.com/begriffs/postgrest/releases/latest

  tar xfJ postgrest-<version>-<platform>.tar.xz

The result will be a file named simply :code:`postgrest` (or :code:`postgrest.exe` on Windows). At this point try running it with

.. code-block:: bash

  ./postgrest

If everything is working correctly it will print out its version and information about configuration. You can continue to run this binary from where you downloaded it, or copy it to a system directory like :code:`/usr/local/bin` on Linux so that you will be able to run it from any directory.

.. note::

  PostgREST requires libpq, the PostgreSQL C library, to be installed on your system. Without the library you'll get an error like "error while loading shared libraries: libpq.so.5." Here's how to fix it:

  .. raw:: html

    <p>
    <details>
      <summary>Ubuntu or Debian</summary>
      <div class="highlight-bash"><div class="highlight">
        <pre>sudo apt-get install libpq-dev</pre>
      </div></div>
    </details>
    <details>
      <summary>Fedora, CentOS, or Red Hat</summary>
      <div class="highlight-bash"><div class="highlight">
        <pre>sudo yum install postgresql-libs</pre>
      </div></div>
    </details>
    <details>
      <summary>OS X</summary>
      <div class="highlight-bash"><div class="highlight">
        <pre>brew install postgresql</pre>
      </div></div>
    </details>
    <details>
      <summary>Windows</summary>
      <p>It isn't fun. Learn more <a href="https://stackoverflow.com/questions/38341725/how-to-install-libpq-dev-package-for-windows">here</a>.</p>
      <p>It might be easier to execute PostgREST in its own Docker image as well.</p>
    </details>
    </p>

Step 4. Create Database for API
-------------------------------

Connect to to SQL console (psql) inside the container. To do so, run this from your command line:

.. code-block:: bash

  sudo docker exec -it tutorial psql -U postgres

You should see the psql command prompt:

::

  psql (9.6.3)
  Type "help" for help.

  postgres=#

The first thing we'll do is create a `named schema <https://www.postgresql.org/docs/current/static/ddl-schemas.html>`_ for the database objects which will be exposed in the API. We can choose any name we like, so how about "api." Execute this and the other SQL statements inside the psql prompt you started.

.. code-block:: postgres

  create schema api;

Our API will have one endpoint, :code:`/todos`, which will come from a table.

.. code-block:: postgres

  create table api.todos (
    id serial primary key,
    done boolean not null default false,
    task text not null,
    due timestamptz
  );

  insert into api.todos (task) values
    ('finish tutorial 0'), ('pat self on back');

Next make a role to use for anonymous web requests. When a request comes in, PostgREST will switch into this role in the database to run queries.

.. code-block:: postgres

  create role web_anon nologin;
  grant web_anon to postgres;

  grant usage on schema api to web_anon;
  grant select on api.todos to web_anon;

The :code:`web_anon` role has permission to access things in the :code:`api` schema, and to read rows in the :code:`todos` table.

Now quit out of psql; it's time to start the API!

.. code-block:: psql

  \q

Step 5. Run PostgREST
---------------------

PostgREST uses a configuration file to tell it how to connect to the database. Create a file :code:`tutorial.conf` with this inside:

.. code-block:: ini

  db-uri = "postgres://postgres:mysecretpassword@localhost/postgres"
  db-schema = "api"
  db-anon-role = "web_anon"

The configuration file has other :ref:`options <configuration>`, but this is all we need. Now run the server:

.. code-block:: bash

  ./postgrest tutorial.conf

You should see

.. code-block:: text

  Listening on port 3000
  Attempting to connect to the database...
  Connection successful

It's now ready to serve web requests. There are many nice graphical API exploration tools you can use, but for this tutorial we'll use :code:`curl` because it's likely to be installed on your system already. Open a new terminal (leaving the one open that PostgREST is running inside). Try doing an HTTP request for the todos.

.. code-block:: bash

  curl http://localhost:3000/todos

The API replies:

.. code-block:: json

  [
    {
      "id": 1,
      "done": false,
      "task": "finish tutorial 0",
      "due": null
    },
    {
      "id": 2,
      "done": false,
      "task": "pat self on back",
      "due": null
    }
  ]

With the current role permissions, anonymous requests have read-only access to the :code:`todos` table. If we try to add a new todo we are not able.

.. code-block:: bash

  curl http://localhost:3000/todos -X POST \
       -H "Content-Type: application/json" \
       -d '{"task": "do bad thing"}'

Response is 401 Unauthorized:

.. code-block:: json

  {
    "hint": null,
    "details": null,
    "code": "42501",
    "message": "permission denied for relation todos"
  }

There we have it, a basic API on top of the database! In the next tutorials we will see how to extend the example with more sophisticated user access controls, and more tables and queries.
