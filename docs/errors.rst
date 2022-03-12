.. _error_source:

Error Source
============

For the most part, error messages will come directly from the database with the same `format that PostgreSQL uses <https://www.postgresql.org/docs/current/plpgsql-errors-and-messages.html>`_, in other words, PostgREST will convert the ``MESSAGE``, ``DETAIL``, ``HINT`` and ``ERRCODE`` from the PostgreSQL error to JSON format and add an HTTP status code to the response (see :ref:`status_codes`). For instance, this is the error you will get when querying a nonexistent table:

.. code-block:: http

  GET /nonexistent_table?id=eq.1 HTTP/1.1

.. code-block:: json

  {
    "hint": null,
    "details": null,
    "code": "42P01",
    "message": "relation \"api.nonexistent_table\" does not exist"
  }

However, some errors do come from PostgREST itself (such as those related to the :ref:`schema_cache`). These errors have the same structure as the PostgreSQL errors (message, details, hint and code) but are differentiated by the ``PGRST`` prefix in the ``code`` field (see :ref:`pgrst_errors`). For instance, when querying a function that does not exist, the error will be:

.. code-block:: http

  POST /rpc/nonexistent_function HTTP/1.1

.. code-block:: json

  {
    "hint": "If a new function was created in the database with this name and parameters, try reloading the schema cache.",
    "details": null
    "code": "PGRST202",
    "message": "Could not find the api.nonexistent_function() function in the schema cache"
  }

.. _status_codes:

HTTP Status Codes
=================

PostgREST translates `PostgreSQL error codes <https://www.postgresql.org/docs/current/errcodes-appendix.html>`_ into HTTP status as follows:

+--------------------------+-------------------------+---------------------------------+
| PostgreSQL error code(s) | HTTP status             | Error description               |
+==========================+=========================+=================================+
| 08*                      | 503                     | pg connection err               |
+--------------------------+-------------------------+---------------------------------+
| 09*                      | 500                     | triggered action exception      |
+--------------------------+-------------------------+---------------------------------+
| 0L*                      | 403                     | invalid grantor                 |
+--------------------------+-------------------------+---------------------------------+
| 0P*                      | 403                     | invalid role specification      |
+--------------------------+-------------------------+---------------------------------+
| 23503                    | 409                     | foreign key violation           |
+--------------------------+-------------------------+---------------------------------+
| 23505                    | 409                     | uniqueness violation            |
+--------------------------+-------------------------+---------------------------------+
| 25006                    | 405                     | read only sql transaction       |
+--------------------------+-------------------------+---------------------------------+
| 25*                      | 500                     | invalid transaction state       |
+--------------------------+-------------------------+---------------------------------+
| 28*                      | 403                     | invalid auth specification      |
+--------------------------+-------------------------+---------------------------------+
| 2D*                      | 500                     | invalid transaction termination |
+--------------------------+-------------------------+---------------------------------+
| 38*                      | 500                     | external routine exception      |
+--------------------------+-------------------------+---------------------------------+
| 39*                      | 500                     | external routine invocation     |
+--------------------------+-------------------------+---------------------------------+
| 3B*                      | 500                     | savepoint exception             |
+--------------------------+-------------------------+---------------------------------+
| 40*                      | 500                     | transaction rollback            |
+--------------------------+-------------------------+---------------------------------+
| 53*                      | 503                     | insufficient resources          |
+--------------------------+-------------------------+---------------------------------+
| 54*                      | 413                     | too complex                     |
+--------------------------+-------------------------+---------------------------------+
| 55*                      | 500                     | obj not in prerequisite state   |
+--------------------------+-------------------------+---------------------------------+
| 57*                      | 500                     | operator intervention           |
+--------------------------+-------------------------+---------------------------------+
| 58*                      | 500                     | system error                    |
+--------------------------+-------------------------+---------------------------------+
| F0*                      | 500                     | config file error               |
+--------------------------+-------------------------+---------------------------------+
| HV*                      | 500                     | foreign data wrapper error      |
+--------------------------+-------------------------+---------------------------------+
| P0001                    | 400                     | default code for "raise"        |
+--------------------------+-------------------------+---------------------------------+
| P0*                      | 500                     | PL/pgSQL error                  |
+--------------------------+-------------------------+---------------------------------+
| XX*                      | 500                     | internal error                  |
+--------------------------+-------------------------+---------------------------------+
| 42883                    | 404                     | undefined function              |
+--------------------------+-------------------------+---------------------------------+
| 42P01                    | 404                     | undefined table                 |
+--------------------------+-------------------------+---------------------------------+
| 42501                    | | if authenticated 403, | insufficient privileges         |
|                          | | else 401              |                                 |
+--------------------------+-------------------------+---------------------------------+
| other                    | 400                     |                                 |
+--------------------------+-------------------------+---------------------------------+

.. _pgrst_errors:

PostgREST Error Codes
=====================

PostgREST error codes have the form ``PGRSTgxx``, where ``PGRST`` is the prefix that differentiates the error from a PostgreSQL error, ``g`` is the group where the error belongs and ``xx`` is the number that identifies the error in the group.

.. _pgrst0**:

Group 0 - Connection
--------------------

Related to the connection with the database.

+---------------+---------------------------------------------+
| Code          | Description                                 |
+===============+=============================================+
| .. _pgrstx01: | Could not connect with the database due to  |
|               | an incorrect :ref:`db-uri` or due to the    |
| PGRST001      | PostgreSQL service not running.             |
+---------------+---------------------------------------------+
| .. _pgrstx02: | Could not connect with the database due to  |
|               | an internal error.                          |
| PGRST002      |                                             |
+---------------+---------------------------------------------+
| .. _pgrstx03: | Could not connect with the database when    |
|               | building the :ref:`schema_cache` due to the |
| PGRST003      | PostgreSQL service not running.             |
+---------------+---------------------------------------------+

.. _pgrst000:

PGRST000
~~~~~~~~

Could not connect with the database due to an incorrect :ref:`db-uri` or due to the PostgreSQL service not running.

.. _pgrst001:

PGRST001
~~~~~~~~

Could not connect with the database due to an internal error.

.. _pgrst002:

PGRST002
~~~~~~~~

Could not connect with the database when building the :ref:`schema_cache`, due to the PostgreSQL service not running.

.. _pgrst1**:

Group 1 - Api Request
---------------------

Related to the HTTP request elements.

.. _pgrst100:

PGRST100
~~~~~~~~

Parsing error in the query string parameter. See :ref:`h_filter`, :ref:`operators` and :ref:`ordering`.

.. _pgrst101:

PGRST101
~~~~~~~~

For :ref:`functions <s_procs>`, only `GET` and `POST` verbs are allowed. Any other verb will throw this error.

.. _pgrst102:

PGRST102
~~~~~~~~

Related to the request body structure. See :ref:`insert_update`.

.. _pgrst103:

PGRST103
~~~~~~~~

Related to :ref:`limits`.

.. _pgrst104:

PGRST104
~~~~~~~~

Either the :ref:`filter operator <operators>` is missing or it doesn't exist.

.. _pgrst105:

PGRST105
~~~~~~~~

Related to an :ref:`UPSERT using PUT <upsert_put>`.

.. _pgrst106:

PGRST106
~~~~~~~~

The schema specified when :ref:`switching schemas <multiple-schemas>` is not present in the :ref:`db-schemas` configuration variable.

.. _pgrst107:

PGRST107
~~~~~~~~

The ``Content-Type`` sent in the request is invalid.

.. _pgrst108:

PGRST108
~~~~~~~~

The filter is applied to a embedded resource that is not specified in the ``select`` part of the query string. See :ref:`embed_filters`.

.. _pgrst2**:

Group 2 - Schema Cache
----------------------

Related to a :ref:`stale schema cache <stale_schema>`. Most of the time, these errors are solved by :ref:`reloading the schema cache <schema_reloading>`.

.. _pgrst200:

PGRST200
~~~~~~~~

Caused by :ref:`stale_fk_relationships`, otherwise any of the embedding resources or the relationship itself may not exist in the database.

.. _pgrst201:

PGRST201
~~~~~~~~

Related to :ref:`embed_disamb`.

.. _pgrst202:

PGRST202
~~~~~~~~

Caused by a :ref:`stale_function_signature`, otherwise the function may not exist in the database.

.. _pgrst203:

PGRST203
~~~~~~~~

Caused by requesting overloaded functions with the same name but different argument types, or by using a ``POST`` verb to request overloaded functions with a ``JSON`` or ``JSONB`` type unnamed parameter. The solution to both is to rename the function or modify the argument names in the database for the first.

.. _pgrst3**:

Group 3 - JWT errors
--------------------

Related to the authentication process using JWT. You can follow the :ref:`tut1` for an example on how to implement authentication and the :doc:`Authentication page <auth>` for more information on this process.

.. _pgrst300:

PGRST300
~~~~~~~~

A :ref:`JWT secret <jwt-secret>` is missing from the configuration.

.. _pgrst301:

PGRST301
~~~~~~~~

Any error related to the verification of the JWT, which means that the JWT provided is invalid in some way.

.. _pgrst302:

PGRST302
~~~~~~~~

Attempted to do a request without :ref:`authentication <client_auth>` when the anonymous role is disabled by not setting it in :ref:`db-anon-role`.

.. _pgrst4**:

Group 4 - Hasql
---------------

Related to `the library <https://hackage.haskell.org/package/hasql>`_ that PostgREST uses to connect to the database. If you encounter any of these errors, you may have stumbled on a PostgREST bug, please `open an issue <https://github.com/PostgREST/postgrest/issues>`_ and we'll be glad to fix it.

.. _pgrst400:

PGRST400
~~~~~~~~

Internal error: Unexpected Result.

.. _pgrst401:

PGRST401
~~~~~~~~

Internal error: Attempted to parse more columns than there are in the result.

.. _pgrst402:

PGRST402
~~~~~~~~

Internal error: Attempted to parse a NULL as some value.

.. _pgrst403:

PGRST403
~~~~~~~~

Internal error: Wrong value parser used.

.. _pgrst404:

PGRST404
~~~~~~~~

Internal error: Unexpected amount of rows.

.. _pgrst5**:

Group 5 - General
-----------------

These are uncategorized errors.

.. _pgrst500:

PGRST500
~~~~~~~~

Related to :ref:`guc_resp_hdrs`.

.. _pgrst501:

PGRST501
~~~~~~~~

The status code must be a positive integer. See :ref:`guc_resp_status`.

.. _pgrst502:

PGRST502
~~~~~~~~

Related to :ref:`binary_output`. See :ref:`providing_img` for an example on requesting images.

.. _pgrst503:

PGRST503
~~~~~~~~

For an :ref:`UPSERT using PUT <upsert_put>`, when :ref:`limits and offsets <limits>` are used.

.. _pgrst504:

PGRST504
~~~~~~~~

For an :ref:`UPSERT using PUT <upsert_put>`, when the primary key in the query string and the body are different.

.. _pgrst505:

PGRST505
~~~~~~~~

More than 1 or no items where returned when requesting a singular response. See :ref:`singular_plural`.

.. _pgrst506:

PGRST506
~~~~~~~~

The HTTP verb used in the request in not supported.
