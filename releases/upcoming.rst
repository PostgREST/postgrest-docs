.. |br| raw:: html

   <br />

Upcoming
========

These are changes yet unreleased. If you'd like to try them out before a new official release, access `the list of CI runs <https://github.com/PostgREST/postgrest/actions/workflows/ci.yaml?query=branch%3Amain>`_
and select the newest commit, then download the build from the Artifacts section at the bottom of the page (you'll need a GitHub account to download it).

Added
-----

* Allow :ref:`embedding <embedding_partitioned_tables>`, UPSERT, INSERT with Location response, OPTIONS request and OpenAPI support for partitioned tables.
  |br| -- `@laurenceisla <https://github.com/laurenceisla>`_

* Add error codes with the `"PGRST"` prefix to the error response body to differentiate PostgREST errors from PostgreSQL errors (see :ref:`error_source`) and include the `detail` and `hint` fields with `null` values if they are missing from the error response body.
  |br| -- `@laurenceisla <https://github.com/laurenceisla>`_
