Tutorial 1 - The Golden Key
===========================

author  
[begriffs](https://github.com/begriffs)

In `tut0` we created a read-only API with a single endpoint to list
todos. There are many directions we can go to make this API more
interesting, but one good place to start would be allowing some users to
change data in addition to reading it.

Step 1. Add a Trusted User
--------------------------

The previous tutorial created a `web_anon` role in the database with
which to execute anonymous web requests. Let's make a role called
`todo_user` for users who authenticate with the API. This role will have
the authority to do anything to the todo list.

    -- run this in psql using the database created
    -- in the previous tutorial

    create role todo_user nologin;
    grant todo_user to authenticator;

    grant usage on schema api to todo_user;
    grant all on api.todos to todo_user;
    grant usage, select on sequence api.todos_id_seq to todo_user;

Step 2. Make a Secret
---------------------

Clients authenticate with the API using JSON Web Tokens. These are JSON
objects which are cryptographically signed using a password known to
only us and the server. Because clients do not know the password, they
cannot tamper with the contents of their tokens. PostgREST will detect
counterfeit tokens and will reject them.

Let's create a password and provide it to PostgREST. Think of a nice
long one, or use a tool to generate it. **Your password must be at least
32 characters long.**

Note

Unix tools can generate a nice password for you:

    # Allow "tr" to process non-utf8 byte sequences
    export LC_CTYPE=C

    # read random bytes and keep only alphanumerics
    < /dev/urandom tr -dc A-Za-z0-9 | head -c32

Open the `tutorial.conf` (created in the previous tutorial) and add a
line with the password:

    # PASSWORD MUST BE AT LEAST 32 CHARS LONG
    # add this line to tutorial.conf:

    jwt-secret = "<the password you made>"

If the PostgREST server is still running from the previous tutorial,
restart it to load the updated configuration file.

Step 3. Sign a Token
--------------------

Ordinarily your own code in the database or in another server will
create and sign authentication tokens, but for this tutorial we will
make one "by hand." Go to [jwt.io](https://jwt.io/#debugger-io) and fill
in the fields like this:

![How to create a token at
<https://jwt.io>](../_static/tuts/tut1-jwt-io.png)

**Remember to fill in the password you generated rather than the word
"secret".** After you have filled in the password and payload, the
encoded data on the left will update. Copy the encoded token.

Note

While the token may look well obscured, it's easy to reverse engineer
the payload. The token is merely signed, not encrypted, so don't put
things inside that you don't want a determined client to see.

Step 4. Make a Request
----------------------

Back in the terminal, let's use `curl` to add a todo. The request will
include an HTTP header containing the authentication token.

    export TOKEN="<paste token here>"

    curl http://localhost:3000/todos -X POST \
         -H "Authorization: Bearer $TOKEN"   \
         -H "Content-Type: application/json" \
         -d '{"task": "learn how to auth"}'

And now we have completed all three items in our todo list, so let's set
`done` to true for them all with a `PATCH` request.

    curl http://localhost:3000/todos -X PATCH \
         -H "Authorization: Bearer $TOKEN"    \
         -H "Content-Type: application/json"  \
         -d '{"done": true}'

A request for the todos shows three of them, and all completed.

    curl http://localhost:3000/todos

    [
      {
        "id": 1,
        "done": true,
        "task": "finish tutorial 0",
        "due": null
      },
      {
        "id": 2,
        "done": true,
        "task": "pat self on back",
        "due": null
      },
      {
        "id": 3,
        "done": true,
        "task": "learn how to auth",
        "due": null
      }
    ]

Step 4. Add Expiration
----------------------

Currently our authentication token is valid for all eternity. The
server, as long as it continues using the same JWT password, will honor
the token.

It's better policy to include an expiration timestamp for tokens using
the `exp` claim. This is one of two JWT claims that PostgREST treats
specially.

<table>
<colgroup>
<col style="width: 18%" />
<col style="width: 81%" />
</colgroup>
<thead>
<tr class="header">
<th>Claim</th>
<th>Interpretation</th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td><code>role</code></td>
<td>The database role under which to execute SQL for API request</td>
</tr>
<tr class="even">
<td><code>exp</code></td>
<td>Expiration timestamp for token, expressed in "Unix epoch time"</td>
</tr>
</tbody>
</table>

Note

Epoch time is defined as the number of seconds that have elapsed since
00:00:00 Coordinated Universal Time (UTC), January 1st 1970, minus the
number of leap seconds that have taken place since then.

To observe expiration in action, we'll add an `exp` claim of five
minutes in the future to our previous token. First find the epoch value
of five minutes from now. In psql run this:

    select extract(epoch from now() + '5 minutes'::interval) :: integer;

Go back to jwt.io and change the payload to

    {
      "role": "todo_user",
      "exp": 123456789
    }

**NOTE**: Don't forget to change the dummy epoch value `123456789` in
the snippet above to the epoch value returned by the psql command.

Copy the updated token as before, and save it as a new environment
variable.

    export NEW_TOKEN="<paste new token>"

Try issuing this request in curl before and after the expiration time:

    curl http://localhost:3000/todos \
         -H "Authorization: Bearer $NEW_TOKEN"

After expiration, the API returns HTTP 401 Unauthorized:

    {"message":"JWT expired"}

Bonus Topic: Immediate Revocation
---------------------------------

Even with token expiration there are times when you may want to
immediately revoke access for a specific token. For instance, suppose
you learn that a disgruntled employee is up to no good and his token is
still valid.

To revoke a specific token we need a way to tell it apart from others.
Let's add a custom `email` claim that matches the email of the client
issued the token.

Go ahead and make a new token with the payload

    {
      "role": "todo_user",
      "email": "disgruntled@mycompany.com"
    }

Save it to an environment variable:

    export WAYWARD_TOKEN="<paste new token>"

PostgREST allows us to specify a stored procedure to run during
attempted authentication. The function can do whatever it likes,
including raising an exception to terminate the request.

First make a new schema and add the function:

    create schema auth;
    grant usage on schema auth to web_anon, todo_user;

    create or replace function auth.check_token() returns void
      language plpgsql
      as $$
    begin
      if current_setting('request.jwt.claim.email', true) =
         'disgruntled@mycompany.com' then
        raise insufficient_privilege
          using hint = 'Nope, we are on to you';
      end if;
    end
    $$;

Next update `tutorial.conf` and specify the new function:

    # add this line to tutorial.conf

    pre-request = "auth.check_token"

Restart PostgREST for the change to take effect. Next try making a
request with our original token and then with the revoked one.

    # this request still works

    curl http://localhost:3000/todos -X PATCH \
         -H "Authorization: Bearer $TOKEN"    \
         -H "Content-Type: application/json"  \
         -d '{"done": true}'

    # this one is rejected

    curl http://localhost:3000/todos -X PATCH      \
         -H "Authorization: Bearer $WAYWARD_TOKEN" \
         -H "Content-Type: application/json"       \
         -d '{"task": "AAAHHHH!", "done": false}'

The server responds with 403 Forbidden:

    {
      "hint": "Nope, we are on to you",
      "details": null,
      "code": "42501",
      "message": "insufficient_privilege"
    }
