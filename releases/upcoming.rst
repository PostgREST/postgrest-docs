.. |br| raw:: html

   <br />

v9.0.0
=======

This mayor version is released following the PostgreSQL 14 launch and is accompanied with new features, improvements to functionality and bug fixes. Downlaod the new version here.

Important Highlights
--------------------

PostgreSQL 14 Compatibility
~~~~~~~~~~~~~~~~~~~~~~~~~~~

The latest PostreSQL release tightened the GUC naming scheme making it impossible to use dots (``.``) and dashes (``-``). Thankfully, `@robertsosinski <https://github.com/robertsosinski>`_ got the PostgreSQL team to reconsider allowing dots in the GUC name, making it possible to avoid a breaking change. You can see the full discussion `here <https://www.postgresql.org/message-id/17045-6a4a9f0d1513f72b%40postgresql.org>`_.

Embedding on Partitioned Tables
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can now confidently embed `partitioned tables <https://www.postgresql.org/docs/10/ddl-partitioning.html>`_ with another tables; meanwhile, their partitions will stay hidden and won't interfere in the process.

Dropping support for PostgreSQL 9.5
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Due to the recent `end of life of PostgreSQL 9.6 <https://www.postgresql.org/support/versioning/>`_, we are dropping support for the next older version. Take into consideration that we are also planning on dropping the support for 9.6 in the next minor versions.

Full Changelog
--------------

New Features
~~~~~~~~~~~~

* `[#1857] <https://github.com/PostgREST/postgrest/issues/1857>`_ Make GUC names for headers, cookies and jwt claims compatible with PostgreSQL v14.

  + The GUC names on PostgreSQL 14 are changed to the ones :ref:`mentioned in this section <guc_req_headers_cookies_claims>`, while older versions still use the :ref:`guc_legacy_names`.
  + PostgreSQL versions below 14 can opt in to the new JSON GUCs by setting the :ref:`db-use-legacy-gucs` config option to false (true by default).

* `[#1783] <https://github.com/PostgREST/postgrest/issues/1783>`_ Allow :ref:`embedding <embedding_partitioned_tables>`, UPSERT, INSERT with Location response, OPTIONS request and OpenAPI support for partitioned tables.

* `[#1878] <https://github.com/PostgREST/postgrest/issues/1878>`_ Add ``Retry-After`` header when recovering the connection. See :ref:`automatic_recovery`.

* `[#1735] <https://github.com/PostgREST/postgrest/issues/1735>`_ Allow calling a function with a :ref:`single unnamed parameter <s_proc_single_unnamed>` to POST raw ``json/jsonb``, ``bytea`` or ``text``.

* `[#1938] <https://github.com/PostgREST/postgrest/issues/1938>`_ Allow escaping inside double quotes with a backslash, e.g. ``?col=in.("Double\"Quote")``, ``?col=in.("Back\\slash")``. See :ref:`reserved-chars`.

* `[#1075] <https://github.com/PostgREST/postgrest/issues/1075>`_ Allow filtering top-level resource based on embedded resources filters. This is enabled by adding ``!inner`` to the embedded resource. See :ref:`embedding_top_level_filter`.

* `[#1988] <https://github.com/PostgREST/postgrest/issues/1988>`_ Allow specifying ``unknown`` for the ``is`` :ref:`operator <operators>`.

* `[#2031] <https://github.com/PostgREST/postgrest/issues/2031>`_ Improve error message for ambiguous embedding and add a relevant hint that includes unambiguous embedding suggestions.

Bug fixes
~~~~~~~~~

* `[#1871] <https://github.com/PostgREST/postgrest/issues/1871>`_ Fix OpenAPI missing default values for String types and identify Array types as "array" instead of "string"

* `[#1930] <https://github.com/PostgREST/postgrest/issues/1930>`_ Fix RPC return type handling for RETURNS TABLE with a single column (regression of #1615).

* `[#1938] <https://github.com/PostgREST/postgrest/issues/1938>`_ Fix using single double quotes (``"``) and backslashes (``/``) as values on the "in" operator

* `[#1992] <https://github.com/PostgREST/postgrest/issues/1992>`_ Fix schema cache query failing with standard_conforming_strings = off

Incompatibilities
~~~~~~~~~~~~~~~~~

* `[#1783] <https://github.com/PostgREST/postgrest/issues/1783>`_ Partitions (created using ``PARTITION OF``) are no longer included in the :ref:`schema_cache`.

* `[#2038] <https://github.com/PostgREST/postgrest/issues/2038>`_ Dropped support for PostgreSQL 9.5

Documentation improvements
~~~~~~~~~~~~~~~~~~~~~~~~~~

* Added :ref:`nested_embedding` to the :ref:`resource_embedding` section.
* Added the :ref:`templates` section to the :doc:`Ecosystem </ecosystem>`.
* Added the :ref:`logical_operators` section

Thanks
------

Thanks to the contributors who made this release possible!

* `@gautam1168 <https://github.com/gautam1168>`_
* `@laurenceisla <https://github.com/laurenceisla>`_
* `@monacoremo <https://github.com/monacoremo>`_
* `@robertsosinski <https://github.com/robertsosinski>`_
* `@steve-chavez <https://github.com/steve-chavez>`_
* `@wolfgangwalther <https://github.com/wolfgangwalther>`_

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
    :target: https://supabase.io/?utm_source=postgrest%20backers&utm_medium=open%20source%20partner&utm_campaign=postgrest%20backers%20github&utm_term=homepage
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
