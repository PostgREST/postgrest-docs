Working with PostgreSQL data types
==================================

You may be wondering if PostgREST allows the use of special literal values, such as ``now`` for timestamps, ``yes`` for booleans or time values including the time zone. The answer is yes to all of them, that is because PostgREST makes use of PostgreSQL text representation to work with data types.

Timestamps
----------

As mentioned above, you can use the time zone to filter or send data if needed. Let's use this table as an example:

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

But what if you need to cast the ``today`` special value to a timezone different from the server. In that case your best bet would be to create a view, a function or :ref:`computed columns <computed_cols>` which we will use in the next example:

.. code-block:: postgres

  create table api.chat (
     id int primary key ,
     user_code varchar(4) unique,
     message text,
     date timestamp
  );

  -- Create the computed column
  create function date_gt_now(api.chat) returns bool as $$
    select $1.date > now() at time zone 'Africa/Cairo';
  $$ language sql;


