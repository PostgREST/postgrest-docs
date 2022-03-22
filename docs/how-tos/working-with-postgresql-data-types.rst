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

JSON
----

To work with a ``json`` type column, you can handle the value as a JSON object. For instance, let's use this table:

.. code-block:: postgres

  create table products (
    id int primary key,
    name text unique,
    extra_info json
  );

Now, you can insert a new product using a JSON object for the ``extra_info`` column:

.. tabs::

  .. code-tab:: http

    POST /products HTTP/1.1
    Content-Type: application/json

    {
      "id": 1,
      "name": "Canned fish",
      "extra_info": {
        "expiry_date": "2025-12-31",
        "exportable": true
      }
    }

  .. code-tab:: bash Curl

    curl "http://localhost:3000/products" \
      -X POST -H "Content-Type: application/json" \
      -d @- << EOF
      {
        "id": 1,
        "name": "Canned fish",
        "extra_info": {
          "expiry_date": "2025-12-31",
          "exportable": true
        }
      }
    EOF

To query and filter the data see :ref:`json_columns` for a complete reference.

Composite Types
---------------

With PostgREST, you have two options to handle `composite type columns <https://www.postgresql.org/docs/current/rowtypes.html>`_. On one hand you can use string representation and on the other you can handle it as you would a JSON column. Let's create a type and a table for this example:

.. code-block:: postgres

  create type dimension as (
    length decimal(6,2),
    width decimal (6,2),
    height decimal (6,2),
    unit text
  );

  create table products (
    id int primary key,
    size dimension
  );

  insert into products (id, size)
  values (1, '(5.0,5.0,10.0,"cm")');

Now, you could insert values using string representation as seen in the example above.

.. tabs::

  .. code-tab:: http

    POST /products HTTP/1.1
    Content-Type: application/json

    { "id": 2, "size": "(0.7,0.5,1.8,\"m\")" }

  .. code-tab:: bash Curl

    curl "http://localhost:3000/products" \
      -X POST -H "Content-Type: application/json" \
      -d @- << EOF
      { "id": 2, "size": "(0.7,0.5,1.8,\"m\")" }
    EOF

Or, you could insert the data in JSON format. The following request is equivalent to the previous one:

.. tabs::

  .. code-tab:: http

    POST /products HTTP/1.1
    Content-Type: application/json

      {
        "id": 2,
        "size": {
          "length": 0.7,
          "width": 0.5,
          "height": 1.8,
          "unit": "m"
        }
      }

  .. code-tab:: bash Curl

    curl "http://localhost:3000/products" \
      -X POST -H "Content-Type: application/json" \
      -d @- << EOF
      {
        "id": 2,
        "size": {
          "length": 0.7,
          "width": 0.5,
          "height": 1.8,
          "unit": "m"
        }
      }
    EOF

You can also query data using the arrow operators as you would for :ref:`JSON columns <json_columns>`.

Ranges
------

To illustrate how to work with `ranges <https://www.postgresql.org/docs/current/rangetypes.html>`_, let's use the following table as an example:

.. code-block:: postgres

   create table events (
     id int primary key,
     name text unique,
     duration tsrange
   );

Now, to insert a new event, specify the ``duration`` value as a string representation of the ``tsrange`` type, for example:

.. tabs::

  .. code-tab:: http

    POST /events HTTP/1.1
    Content-Type: application/json

    {
      "id": 1,
      "name": "New Year's Party",
      "duration": "['2022-12-31 11:00','2023-01-01 06:00']"
    }

  .. code-tab:: bash Curl

    curl "http://localhost:3000/events" \
      -X POST -H "Content-Type: application/json" \
      -d @- << EOF
      {
        "id": 1,
        "name": "New Year's Party",
        "duration": "['2022-12-31 11:00','2023-01-01 06:00']"
      }
    EOF

You can use range :ref:`operators <operators>` to filter the data. But what if you need get the events for the New Year 2023? Doing this filter ``events?duration=cs.2023-01-01`` will return an error because PostgreSQL needs an explicit cast to timestamp of the string value. A workaround would be to use a range starting and ending in the same date, like this:

.. tabs::

  .. code-tab:: http

    GET /events?duration=cs.[2023-01-01,2023-01-01] HTTP/1.1

  .. code-tab:: bash Curl

    curl "http://localhost:3000/events?duration=cs.\[2023-01-01,2023-01-01\]"

.. code-block:: json

  [
    {
      "id": 1,
      "name": "New Year's Party",
      "duration": "[\"2022-12-31 11:00:00\",\"2023-01-01 06:00:00\"]"
    }
  ]

.. _casting_range_to_json:

Casting a Range to a JSON Object
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

As you may have noticed, the ``tsrange`` value is returned as a string literal. To return it as a JSON value, first you need to create a function that will do the conversion from a ``tsrange`` type:

.. code-block:: postgres

   create or replace function tsrange_to_json(tsrange) returns json as $$
     select json_build_object(
       'lower', lower($1)
     , 'upper', upper($1)
     , 'lower_inc', lower_inc($1)
     , 'upper_inc', upper_inc($1)
     );
   $$ language sql;

Then, create the cast using this function:

.. code-block:: postgres

   create cast (tsrange as json) with function tsrange_to_json(tsrange) as assignment;

Finally, do the request :ref:`casting the range column <casting_columns>`:

.. tabs::

  .. code-tab:: http

    GET /events?select=id,name,duration::json HTTP/1.1

  .. code-tab:: bash Curl

    curl "http://localhost:3000/events?select=id,name,duration::json"

.. code-block:: json

  [
    {
      "id": 1,
      "name": "New Year's Party",
      "duration": {
        "lower": "2022-12-31T11:00:00",
        "upper": "2023-01-01T06:00:00",
        "lower_inc": true,
        "upper_inc": true
      }
    }
  ]

.. note::

   If you don't want to modify casts for built-in types, an option would be to `create a custom type <https://www.postgresql.org/docs/current/sql-createtype.html>`_
   for your own ``tsrange`` and add its own cast.

   .. code-block:: postgres

      create type mytsrange as range (subtype = timestamp, subtype_diff = tsrange_subdiff);

      -- define column types and casting function analogously to the above example
      -- ...

      create cast (mytsrange as json) with function mytsrange_to_json(mytsrange) as assignment;
