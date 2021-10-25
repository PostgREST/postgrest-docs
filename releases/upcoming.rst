.. |br| raw:: html

   <br />

Upcoming
========

Added
-----

* Allow :ref:`embedding <embedding_partitioned_tables>`, UPSERT, INSERT with Location response, OPTIONS request and OpenAPI support for partitioned tables.
  |br| -- `@laurenceisla <https://github.com/laurenceisla>`_

* Allow calling a function with a single unnamed parameter to POST raw :ref:`json/jsonb <s_proc_single_unnamed_json>`, :ref:`bytea <s_proc_single_unnamed_binary>` or :ref:`text <s_proc_single_unnamed_text>`.
  |br| -- `@steve-chavez <https://github.com/steve-chavez>`_

Changed
-------

* Functions with a single unnamed JSON parameter :ref:`must not be overloaded <s_proc_single_unnamed_json_overloaded>`.
  |br| -- `@steve-chavez <https://github.com/steve-chavez>`_
