.. _working_with_types:

Working with PostgreSQL data types
==================================

PostgREST makes use of PostgreSQL text representation to work with data types. Thanks to this, you can use special literal values, such as ``now`` for timestamps, ``yes`` for booleans or time values including the time zones. This page describes how you can use literal values for different PostgreSQL types.

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

But what if, for any reason, you need to cast a special value like ``now`` to a timezone different from the server. There is no way to do this using PostgreSQL text representation, the only alternative would be to use the ``AT TIME ZONE`` construct, so your best bet would be to create a view, a :ref:`function <s_procs>` or :ref:`computed columns <computed_cols>`. Let's use the last one for the next example:

.. code-block:: postgres

  drop table if exists reports;

  -- For this example, the due_date is a timestamp type
  create table reports (
    id int primary key
    , due_date timestamp
  );

  -- Create the computed column (must be created in the exposed schema)
  create function due_date_gt_now (report) returns bool as $$
    select $1.due_date > now() at time zone 'Australia/Sydney';
  $$ language sql;

  insert into reports (id, due_date) values (1, '2022-02-27 22:00:00');

Now it's possible to filter the data using the computed column:

.. tabs::

  .. code-tab:: http

    GET /reports?select=*,due_date_gt_now&due_date_gt_now=is.true HTTP/1.1

  .. code-tab:: bash Curl

    curl "http://localhost:3000/reports?select=*,due_date_gt_now&due_date_gt_now=is.true"

.. code-block:: json

  [
    {
      "id": 1,
      "due_date": "2022-02-27T22:00:00",
      "due_date_gt_now": true
    }
  ]
