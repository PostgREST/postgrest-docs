Configuration
=============

PostgREST reads a configuration file to determine information about the
database and how to serve client requests. There is no predefined
location for this file, you must specify the file path as the one and
only argument to the server:

    ./postgrest /path/to/postgrest.conf

The configuration file must contain a set of key value pairs. At minimum
you must include these keys:

    # postgrest.conf

    # The standard connection URI format, documented at
    # https://www.postgresql.org/docs/current/static/libpq-connect.html#AEN45347
    db-uri       = "postgres://user:pass@host:5432/dbname"

    # The name of which database schema to expose to REST clients
    db-schema    = "api"

    # The database role to use when no client authentication is provided.
    # Can (and should) differ from user in db-uri
    db-anon-role = "anon"

The user specified in the db-uri is also known as the authenticator
role. For more information about the anonymous vs authenticator roles
see the `roles`.

Here is the full list of configuration parameters.

<table>
<thead>
<tr class="header">
<th>Name</th>
<th>Type</th>
<th>Default</th>
<th>Required</th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td><p>db-uri db-schema db-anon-role db-pool db-pool-timeout db-extra-search-path server-host server-port server-unix-socket server-unix-socket-mode openapi-server-proxy-uri jwt-secret jwt-aud secret-is-base64 max-rows pre-request app.settings.* role-claim-key raw-media-types</p></td>
<td><p>String String String Int Int String String Int String String</p>
<p>String String Bool Int String String String String</p></td>
<td><p>10 10 public !4 3000</p>
<p>660 String</p>
<p>False ∞</p>
<p>.role</p></td>
<td><p>Y Y Y</p></td>
</tr>
</tbody>
</table>

db-uri
------

> The standard connection PostgreSQL [URI
> format](https://www.postgresql.org/docs/current/static/libpq-connect.html#AEN45347).
> Symbols and unusual characters in the password or other fields should
> be percent encoded to avoid a parse error. If enforcing an SSL
> connection to the database is required you can use
> [sslmode](https://www.postgresql.org/docs/9.1/static/libpq-ssl.html#LIBPQ-SSL-SSLMODE-STATEMENTS)
> in the URI, for example
> `postgres://user:pass@host:5432/dbname?sslmode=require`.
>
> When running PostgREST on the same machine as PostgreSQL, it is also
> possible to connect to the database using a [Unix
> socket](https://en.wikipedia.org/wiki/Unix_domain_socket) and the
> [Peer Authentication
> method](http://www.postgresql.org/docs/current/static/auth-methods.html#AUTH-PEER)
> as an alternative to TCP/IP communication and authentication with a
> password, this also grants higher performance. To do this you can omit
> the host and the password, e.g. `postgres://user@/dbname`, see the
> [libpq connection
> string](https://www.postgresql.org/docs/10/static/libpq-connect.html#LIBPQ-CONNSTRING)
> documentation for more details.
>
> On older systems like Centos 6, with older versions of libpq, a
> different db-uri syntax has to be used. In this case the URI is a
> string of space separated key-value pairs (key=value), so the example
> above would be
> `"host=host user=user port=5432 dbname=dbname password=pass"`.
>
> Choosing a value for this parameter beginning with the at sign such as
> `@filename` (e.g. `@./configs/my-config`) loads the secret out of an
> external file.

db-schema
---------

> The database schema to expose to REST clients. Tables, views and
> stored procedures in this schema will get API endpoints.
>
> This schema gets added to the
> [search\_path](https://www.postgresql.org/docs/11/ddl-schemas.html#DDL-SCHEMAS-PATH)
> of every request.

db-anon-role
------------

> The database role to use when executing commands on behalf of
> unauthenticated clients. For more information, see `roles`.

db-pool
-------

> Number of connections to keep open in PostgREST's database pool.
> Having enough here for the maximum expected simultaneous client
> connections can improve performance. Note it's pointless to set this
> higher than the `max_connections` GUC in your database.

db-pool-timeout
---------------

> Time to live, in seconds, for an idle database pool connection. If the
> timeout is reached the connection will be closed. Once a new request
> arrives a new connection will be started.

db-extra-search-path
--------------------

> Extra schemas to add to the
> [search\_path](https://www.postgresql.org/docs/11/ddl-schemas.html#DDL-SCHEMAS-PATH)
> of every request. These schemas tables, views and stored procedures
> **don't get API endpoints**, they can only be referred from the
> database objects inside your `db-schema`.
>
> This parameter was meant to make it easier to use **PostgreSQL
> extensions** (like PostGIS) that are outside of the `db-schema`.
>
> Multiple schemas can be added in a comma-separated string, e.g.
> `public, extensions`.

server-host
-----------

> Where to bind the PostgREST web server. In addition to the usual
> address options, PostgREST interprets these reserved addresses with
> special meanings:
>
> -   `*` - any IPv4 or IPv6 hostname
> -   `*4` - any IPv4 or IPv6 hostname, IPv4 preferred
> -   `!4` - any IPv4 hostname
> -   `*6` - any IPv4 or IPv6 hostname, IPv6 preferred
> -   `!6` - any IPv6 hostname

server-port
-----------

> The TCP port to bind the web server.

server-unix-socket
------------------

> [Unix domain socket](https://en.wikipedia.org/wiki/Unix_domain_socket)
> where to bind the PostgREST web server. If specified, this takes
> precedence over `server-port`. Example:
>
>     server-unix-socket = "/tmp/pgrst.sock"

server-unix-socket-mode
-----------------------

> [Unix file
> mode](https://en.wikipedia.org/wiki/File_system_permissions) to be set
> for the socket specified in `server-unix-socket` Needs to be a valid
> octal between 600 and 777.
>
>     server-unix-socket-mode = "660"

openapi-server-proxy-uri
------------------------

> Overrides the base URL used within the OpenAPI self-documentation
> hosted at the API root path. Use a complete URI syntax
> `scheme:[//[user:password@]host[:port]][/]path[?query][#fragment]`.
> Ex. `https://postgrest.com`
>
>     {
>       "swagger": "2.0",
>       "info": {
>         "version": "0.4.3.0",
>         "title": "PostgREST API",
>         "description": "This is a dynamic API generated by PostgREST"
>       },
>       "host": "postgrest.com:443",
>       "basePath": "/",
>       "schemes": [
>         "https"
>       ]
>     }

jwt-secret
----------

> The secret or [JSON Web Key (JWK) (or
> set)](https://tools.ietf.org/html/rfc7517) used to decode JWT tokens
> clients provide for authentication. For security the key must be **at
> least 32 characters long**. If this parameter is not specified then
> PostgREST refuses authentication requests. Choosing a value for this
> parameter beginning with the at sign such as `@filename` loads the
> secret out of an external file. This is useful for automating
> deployments. Note that any binary secrets must be base64 encoded. Both
> symmetric and asymmetric cryptography are supported. For more info see
> `asym_keys`.

jwt-aud
-------

> Specifies the [JWT audience
> claim](https://tools.ietf.org/html/rfc7519#section-4.1.3). If this
> claim is present in the client provided JWT then you must set this to
> the same value as in the JWT, otherwise verifying the JWT will fail.

secret-is-base64
----------------

> When this is set to `true`, the value derived from `jwt-secret` will
> be treated as a base64 encoded secret.

max-rows
--------

> A hard limit to the number of rows PostgREST will fetch from a view,
> table, or stored procedure. Limits payload size for accidental or
> malicious requests.

pre-request
-----------

> A schema-qualified stored procedure name to call right after switching
> roles for a client request. This provides an opportunity to modify SQL
> variables or raise an exception to prevent the request from
> completing.

app.settings.\*
---------------

> Arbitrary settings that can be used to pass in secret keys directly as
> strings, or via OS environment variables. For instance:
> `app.settings.jwt_secret = "$(MYAPP_JWT_SECRET)"` will take
> `MYAPP_JWT_SECRET` from the environment and make it available to
> postgresql functions as `current_setting('app.settings.jwt_secret')`.

role-claim-key
--------------

> A JSPath DSL that specifies the location of the `role` key in the JWT
> claims. This can be used to consume a JWT provided by a third party
> service like Auth0, Okta or Keycloak. Usage examples:
>
>     # {"postgrest":{"roles": ["other", "author"]}}
>     # the DSL accepts characters that are alphanumerical or one of "_$@" as keys
>     role-claim-key = ".postgrest.roles[1]"
>
>     # {"https://www.example.com/role": { "key": "author }}
>     # non-alphanumerical characters can go inside quotes(escaped in the config value)
>     role-claim-key = ".\"https://www.example.com/role\".key"

raw-media-types
---------------

> This serves to extend the [Media
> Types](https://en.wikipedia.org/wiki/Media_type) that PostgREST
> currently accepts through an `Accept` header.
>
> These media types can be requested by following the same rules as the
> ones defined in `binary_output`.
>
> As an example, the below config would allow you to request an
> **image** and an **xml** by doing a request with `Accept: image/png`
> and a request with `Accept: text/xml`, respectively.
>
>     raw-media-types="image/png, text/xml"
