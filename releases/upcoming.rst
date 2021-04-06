.. |br| raw:: html

   <br />

Upcoming
========

These are changes yet unreleased. If you'd like to try them out before a new official release, you can use a `nightly release <https://github.com/PostgREST/postgrest/releases/tag/nightly>`_.

Added
-----

* Allow HTTP status override through the :ref:`response.status <guc_resp_status>` GUC.
  |br| -- `@steve-chavez <https://github.com/steve-chavez>`_
* Allow :ref:`s_procs_variadic`.
  |br| -- `@wolfgangwalther <https://github.com/wolfgangwalther>`_

Fixed
-----

* Fix showing UNKNOWN on ``postgrest --help`` invocation.
  |br| -- `@monacoremo <https://github.com/monacoremo>`_

Changed
-------

* Docker images are now optimized to be built from the scratch image. This reduces the compressed image size from over 30 MB to about 4 MB.
  For more details, see `Docker image built with Nix <https://github.com/PostgREST/postgrest/tree/master/nix/docker#docker-image-built-with-nix>`_.
  |br| -- `@monacoremo <https://github.com/monacoremo>`_
