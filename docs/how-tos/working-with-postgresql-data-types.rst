.. _working_with_types:

Working with PostgreSQL data types
==================================

PostgREST makes use of PostgreSQL string representations to work with data types. Thanks to this, you can use special values, such as ``now`` for timestamps, ``yes`` for booleans or time values including the time zones. This page describes how you can take advantage of these string representations to perform operations on different PostgreSQL data types.

Timestamps
----------

You can use the **time zone** to filter or send data if needed. Let's use this table as an example:

.. code-block:: postgres

  create table reports (
    id int primary key
    , due_date timestamptz
  );

Suppose you are located in Sydney and want create a report with the date in the local time zone. Your request should look like this:

.. tabs::

  .. code-tab:: http

    POST /reports HTTP/1.1
    Content-Type: application/json

    [{ "id": 1, "due_date": "2022-02-24 11:10:15 Australia/Sydney" },
     { "id": 2, "due_date": "2022-02-27 22:00:00 Australia/Sydney" }]

  .. code-tab:: bash Curl

    curl "http://localhost:3000/reports" \
      -X POST -H "Content-Type: application/json" \
      -d '[{ "id": 1, "due_date": "2022-02-24 11:10:15 Australia/Sydney" },{ "id": 2, "due_date": "2022-02-27 22:00:00 Australia/Sydney" }]'

Someone located in Cairo can retrieve the data using their local time, too:

.. tabs::

  .. code-tab:: http

    GET /reports?due_date=eq.2022-02-24+02:10:15+Africa/Cairo HTTP/1.1

  .. code-tab:: bash Curl

    curl "http://localhost:3000/reports?due_date=eq.2022-02-24+02:10:15+Africa/Cairo"

.. code-block:: json

  [
    {
      "id": 1,
      "due_date": "2022-02-23T19:10:15-05:00"
    }
  ]

The response has the date in the time zone configured by the server: ``UTC -05:00``.

You can use other comparative filters and also `PostgreSQL special date/time input values <https://www.postgresql.org/docs/current/datatype-datetime.html#DATATYPE-DATETIME-SPECIAL-TABLE>`_. For instance, to get the reports that are due after today you would do:

.. tabs::

  .. code-tab:: http

    GET /reports?due_date=gt.today HTTP/1.1

  .. code-tab:: bash Curl

    curl "http://localhost:3000/reports?due_date=gt.today"

.. code-block:: json

  [
    {
      "id": 2,
      "due_date": "2022-02-27T06:00:00-05:00"
    }
  ]

hstore
------

You can also work with data types belonging to additional supplied modules such as `hstore <https://www.postgresql.org/docs/current/hstore.html>`_. Let's use the following table:

.. code-block:: postgres

  -- Activate the hstore module in the current database
  create extension if not exists hstore;

  create table api.countries (
    id int primary key,
    name hstore unique
  );

The ``name`` column will have the name of the country in different formats. You can insert values using the text representation for that data type, for instance:

.. tabs::

  .. code-tab:: http

    POST /countries HTTP/1.1
    Content-Type: application/json

    [
      { "id": 1, "name": "common => Egypt, official => \"Arab Republic of Egypt\", native => مصر" },
      { "id": 2, "name": "common => Germany, official => \"Federal Republic of Germany\", native => Deutschland" }
    ]

  .. code-tab:: bash Curl

    curl "http://localhost:3000/countries" \
      -X POST -H "Content-Type: application/json" \
      -d @- << EOF
      [
        { "id": 1, "name": "common => Egypt, official => \"Arab Republic of Egypt\", native => مصر" },
        { "id": 2, "name": "common => Germany, official => \"Federal Republic of Germany\", native => Deutschland" }
      ]
    EOF

Notice that the use of ``"`` in the value of the ``name`` column needs to be escaped using a backslash ``\``.

You can also query and filter the value of a ``hstore`` column using the arrow operators, as you would do for a :ref:`JSON column<json_columns>`. For example, if you want to get the native name of Egypt, the query would be:

.. tabs::

  .. code-tab:: http

    GET /countries?select=name->>native&name->>common=like.Egypt HTTP/1.1

  .. code-tab:: bash Curl

    curl "http://localhost:3000/countries?select=name->>native&name->>common=like.Egypt"

.. code-block:: json

  [{ "native": "مصر" }]
