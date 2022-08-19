
Latest
======

These are features/bugfixes not yet on a stable version. You can try them by downloading the latest pre-releases `on the GitHub release page <https://github.com/PostgREST/postgrest/releases>`_.

Features
--------

API
~~~

XML support
^^^^^^^^^^^

REST is not only JSON. On this release, we are starting to add XML support. Selecting a single column from a table or a :ref:`scalar function <scalar_return_formats>` with the ``Accept: text/xml`` header will return XML output. In the same way, including ``Content-Type: text/xml`` allows to send raw XML to a :ref:`function with a single unnamed parameter <s_proc_single_unnamed>`. We also have an example on :ref:`how to generate SOAP endpoints <create_soap_endpoint>` thanks to `fjf2002 <https://github.com/fjf2002>`_, who made this feature a reality.

GeoJSON out of the box
^^^^^^^^^^^^^^^^^^^^^^

We now support GeoJSON output via the PostGIS library (versions 3.0.0 and up). Requests will return a ``FeatureCollection`` type object if you include the ``Accept: application/geo+json`` header. This also extends to returning the created, updated or deleted object (with ``Prefer: return=representation``) and when doing :ref:`resource embedding <resource_embedding>`. The :ref:`working with PostGIS section <ww_postgis>` has a simple example to get you started.

Access composite type fields and array elements
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can now :ref:`access fields of a Composite type or elements of an Array type <composite_array_columns>` with the arrow operators(``->``, ``->>``) in the same way you would access the JSON type fields.

Improved error messages
^^^^^^^^^^^^^^^^^^^^^^^

To increase consistency, all the errors messages are now normalized. The ``hint``, ``details``, ``code`` and ``message`` fields will always be present in the body, each one defaulting to a
``null`` value. In the same way, the :ref:`errors that were raised <raise_error>` with ``SQLSTATE`` now include the ``message`` and ``code`` in the body.

In addition to these changes and to further clarify the source of an error, PostgREST now adds a ``PGRST`` prefix to the error code of all the errors that are PostgREST-specific and don't come from the database. These errors have a unique code that identifies them and are documented in the :ref:`pgrst_errors` section.

Alongside these changes, there is now a dedicated reference page for :doc:`Error documentation </errors>`.

Get the execution plan
^^^^^^^^^^^^^^^^^^^^^^

You can now verify the :ref:`execution plan of a request <explain_plan>` as a result of using `EXPLAIN <https://www.postgresql.org/docs/current/sql-explain.html>`_ on the generated query. The result is available in ``json`` or ``text`` formats and is compatible with `<https://explain.depesz.com/>`_ for a better readability.

Administration
~~~~~~~~~~~~~~

Health checks
^^^^^^^^^^^^^

Admins can now benefit from two :ref:`health check endpoints <health_check>` exposed in a different port than the main app. When activated, the ``live`` and ``ready`` endpoints are available to verify if PostgREST is alive and running or if the database connection and the :ref:`schema cache <schema_cache>` are ready for querying.

Logging users
^^^^^^^^^^^^^

You can now verify the current authenticated database user in the :ref:`request log <pgrst_logging>` on stdout.

Run without configuration
^^^^^^^^^^^^^^^^^^^^^^^^^

It is now possible to execute PostgREST without specifying any configuration variable, even without the three that were mandatory

  - If :ref:`db-uri` is not set, PostgREST will use the `libpq environment variables <https://www.postgresql.org/docs/current/libpq-envars.html>`_ for the database connection.
  - If :ref:`db-schemas` is not set, it will use the database ``public`` schema.
  - If :ref:`db-anon-role` is not set, it will not allow anonymous requests.

Documentation improvements
~~~~~~~~~~~~~~~~~~~~~~~~~~

* Added a :doc:`/how-tos/working-with-postgresql-data-types` how-to, which contains explanations and examples on how to work with different PostgreSQL data types such as timestamps, ranges or PostGIS types, among others.

* Added in-database and environment variable settings for each :ref:`configuration variable <config_full_list>`.

* Added the :ref:`file_descriptors` subsection.

* Moved the :ref:`error_source` and the :ref:`status_codes` sections to the :doc:`errors reference page </errors>`.

* Moved the *Casting type to custom JSON* how-to to the :ref:`casting_range_to_json` subsection.

* Removed direct links for PostgREST versions older than 8.0 from the versions menu.

* Removed the deprecated *Embedding table from another schema* how-to.

Bug fixes
---------

* Return ``204 No Content`` without ``Content-Type`` for ``PUT`` (`#2058 <https://github.com/PostgREST/postgrest/issues/2058>`_)

* Clarify error for failed schema cache load. (`#2107 <https://github.com/PostgREST/postgrest/issues/2107>`_)

  - From ``Database connection lost. Retrying the connection`` to ``Could not query the database for the schema cache. Retrying.``

* Fix silently ignoring filter on a non-existent embedded resource (`#1771 <https://github.com/PostgREST/postgrest/issues/1771>`_)

* Remove functions, which are not callable due to unnamed arguments, from schema cache and OpenAPI output. (`#2152 <https://github.com/PostgREST/postgrest/issues/2152>`_)

* Fix accessing JSON array fields with ``->`` and ``->>`` in ``?select=`` and ``?order=``. (`#2145 <https://github.com/PostgREST/postgrest/issues/2145>`_)

* Ignore ``max-rows`` on ``POST``, ``PATCH``, ``PUT`` and ``DELETE`` (`#2155 <https://github.com/PostgREST/postgrest/issues/2155>`_)

* Fix inferring a foreign key column as a primary key column on views (`#2254 <https://github.com/PostgREST/postgrest/issues/2254>`_)

* Restrict generated many-to-many relationships (`#2070 <https://github.com/PostgREST/postgrest/issues/2070>`_)

  - Only adds many-to-many relationships when a table has foreign keys to two other tables and these foreign key columns are part of the table's primary key columns.

* Allow casting to types with underscores and numbers (e.g. ``select=oid_array::_int4``) (`#2278 <https://github.com/PostgREST/postgrest/issues/2278>`_)

* Prevent views from breaking one-to-many/many-to-one embeds when using column or foreign key as target (`#2277 <https://github.com/PostgREST/postgrest/issues/2277>`_, `#2238 <https://github.com/PostgREST/postgrest/issues/2238>`_, `#1643 <https://github.com/PostgREST/postgrest/issues/1643>`_)

  - When using a column or foreign key as target for embedding (``/tbl?select=*,col-or-fk(*)``), only tables are now detected and views are not.

  - You can still use a column or an inferred foreign key on a view to embed a table (``/view?select=*,col-or-fk(*)``)

* Increase the ``db-pool-timeout`` to 1 hour to prevent frequent high connection latency (`#2317 <https://github.com/PostgREST/postgrest/issues/2317>`_)

* The search path now correctly identifies schemas with uppercase and special characters in their names (regression) (`#2341 <https://github.com/PostgREST/postgrest/issues/2341>`_)

* "404 Not Found" on nested routes and "405 Method Not Allowed" errors no longer start an empty database transaction (`#2364 <https://github.com/PostgREST/postgrest/issues/2364>`_)

* Fix inaccurate result count when an inner embed was selected after a normal embed in the query string (`#2342 <https://github.com/PostgREST/postgrest/issues/2342>`_)

* ``OPTIONS`` requests no longer start an empty database transaction (`#2376 <https://github.com/PostgREST/postgrest/issues/2376>`_)

* Allow using columns with dollar sign ($) without double quoting in filters and ``select`` (`#2395 <https://github.com/PostgREST/postgrest/issues/2395>`_)

* Fix loop crash error on startup in PostgreSQL 15 beta 3. ``Log: "UNION types \"char\" and text cannot be matched."`` (`#2410 <https://github.com/PostgREST/postgrest/issues/2410>`_)

* Fix race conditions managing database connection helper (`#2397 <https://github.com/PostgREST/postgrest/issues/2397>`_)

* Allow ``limit=0`` in the request query to return an empty array (`#2269 <https://github.com/PostgREST/postgrest/issues/2269>`_)

Breaking changes
----------------

* Return ``204 No Content`` without ``Content-Type`` for RPCs returning ``VOID`` (`#2001 <https://github.com/PostgREST/postgrest/issues/2001>`_)

  - Previously, those RPCs would return ``null`` as a body with ``Content-Type: application/json``.

* ``limit/offset`` now limits the affected rows on ``UPDATE``/``DELETE`` (`#2156 <https://github.com/PostgREST/postgrest/issues/2156>`_)

  - Previously, ``limit``/``offset`` only limited the returned rows but not the actual updated rows

* ``max-rows`` is no longer applied on ``POST``, ``PATCH``, ``PUT`` and ``DELETE`` returned rows (`#2155 <https://github.com/PostgREST/postgrest/issues/2155>`_)

  - This was misleading because the affected rows were not really affected by ``max-rows``, only the returned rows were limited

* Restrict generated many-to-many relationships (`#2070 <https://github.com/PostgREST/postgrest/issues/2070>`_)

  - A primary key that contains the foreign key columns is now needed for generating many-to-many relationships.

* Views now are not detected when embedding using the column or foreign key as target (``/view?select=*,column(*)``) (`#2277 <https://github.com/PostgREST/postgrest/issues/2277>`_)

  - This embedding form was easily made ambiguous whenever a new view was added.

  - For migrating, clients must be updated to the embedding form of ``/view?select=*,other_view!column(*)``.

* Using `Prefer: return=representation` no longer returns a `Location` header (`#2312 <https://github.com/PostgREST/postgrest/issues/2312>`_)

Thanks
------

Big thanks from the `PostgREST team <https://github.com/orgs/PostgREST/people>`_ to our sponsors!

.. container:: image-container

  .. image:: ../_static/cybertec-new.png
    :target: https://www.cybertec-postgresql.com/en/?utm_source=postgrest.org&utm_medium=referral&utm_campaign=postgrest
    :width:  13em

  .. image:: ../_static/2ndquadrant.png
    :target: https://www.2ndquadrant.com/en/?utm_campaign=External%20Websites&utm_source=PostgREST&utm_medium=Logo
    :width:  13em

  .. image:: ../_static/retool.png
    :target: https://retool.com/?utm_source=sponsor&utm_campaign=postgrest
    :width:  13em

  .. image:: ../_static/gnuhost.png
    :target: https://gnuhost.eu/?utm_source=sponsor&utm_campaign=postgrest
    :width:  13em

  .. image:: ../_static/supabase.png
    :target: https://supabase.com/?utm_source=postgrest%20backers&utm_medium=open%20source%20partner&utm_campaign=postgrest%20backers%20github&utm_term=homepage
    :width:  13em

  .. image:: ../_static/oblivious.jpg
    :target: https://oblivious.ai/?utm_source=sponsor&utm_campaign=postgrest
    :width:  13em

* Evans Fernandes
* `Jan Sommer <https://github.com/nerfpops>`_
* `Franz Gusenbauer <https://www.igutech.at/>`_
* `Daniel Babiak <https://github.com/dbabiak>`_
* Tsingson Qin
* Michel Pelletier
* Jay Hannah
* Robert Stolarz
* Nicholas DiBiase
* Christopher Reid
* Nathan Bouscal
* Daniel Rafaj
* David Fenko
* Remo Rechkemmer
* Severin Ibarluzea
* Tom Saleeba
* Pawel Tyll

If you like to join them please consider `supporting PostgREST development <https://github.com/PostgREST/postgrest#user-content-supporting-development>`_.
