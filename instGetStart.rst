Getting Started
###############

For all installation details see admin.html#configuration. In this section we offer a "plug and play" fast installation, for your first contact with PostgREST, when using a popular environment like Windos 10 or UBUNTU 16. The preference here is to use terminal mode installations.


Preparing terminal
-------------------

Use yor preffered terminal interface to issue textual commands:

* The standard "Terminal" of Debian, Ubuntu, etc.
* The "Command Prompt" option from the "Accessories" in a Windows environment. 
* A `ssh` section in a remote Linux server.
* "Mac's Terminal"

and go to a "sandbox folder", a directory where you can work with installation files with no permission problem (eg. `cd ~`), or create a new folder for it, eg. `mkdir sandbox`.

Preparing a "restest" database
------------------------------

It is important to check your PostgreSQL server version, must be *v9.5* or later. If you using [PgAdmin](https://www.pgadmin.org/) you can check there, and copy/paste SQL commands (below) in the Query Tool.  See below at section of the system that you using (eg. Ubuntu) how to check versions.

The default user of any PostgreSQL installation is *postgres*, and all environments offer the [interactive terminal `psql`](https://www.postgresql.org/docs/current/static/app-psql.html), so we use it to create a fake database for tests and demonstrations. 


```
psql -h localhost -U postgres

SELECT version(); -- must be 9.5+!

CREATE DATABASE restest;
\c restest
CREATE table t (
  id serial NOT NULL PRIMARY KEY,
  label text NOT NULL,
  note text,
  created date NOT NULL default now(),
  UNIQUE(label)
);
INSERT INTO t (label,note) VALUES 
  ('first','the first'),
  ('second','the 2nd'),
  ('a',NULL),
  ('b','last')
;
\q
```

UBUNTU 16 LTS
--------------

Check your PostgreSQL: `psql --version` (must be 9.5+) and server with `service postgresql status`. Simalerlly check Nginx by  `service nginx status`.  If any one with problem, you must fiz it first.

Let's start the PostgREST installation at (suppose) *sandbox* folder:

```sh
cd ~/sandbox
wget -c https://github.com/begriffs/postgrest/releases/download/v0.4.0.0/postgrest-0.4.0.0-ubuntu.tar.xz
tar xf  postgrest-0.4.0.0-ubuntu.tar.xz
./postgrest --help
```

If PostgREST shows its help message, the installation was fine. Supposing that all PostgreSQL defaults are available, you can crete this simplest configuration file,

```
cat > postgrest.conf
  db-uri = "postgres://postgres:postgres@localhost:5432/restest"
  db-schema = "public"
  db-anon-role = "postgres"
  db-pool = 10
  
  server-host = "*4"
  server-port = 3000
  ^d
```

instead  `cat` and *control-D* you can use some editor as `nano postgrest.conf`. All ok? (use `more postgrest.conf` to check).
Now you can start the PostgREST process with the command,

```
./postgrest postgrest.conf < /dev/null > /var/log/postgrest.log 2>&1 &

```

check `systemctl status postgresql` (if not exit) and the process pid. For only a fast try you can tansform the terminal in a postgrest-console using only ` `./postgrest postgrest.conf`.

To test, check with `more t.json` the content of `wget -O t.json -c http://localhost:3000/t`. For more tests see the section below, *Testing the "restest" database*. 

If it as server and default Nginx is at `http://domain.xpto`  try the `wget` command with it. For more elaborated uses, like by a subdomain `pgrest.domain.xpto`, see [hardening-postgrest](http://postgrest.com/en/v0.4/admin.html#hardening-postgrest).


Windows 7
---------

... if you created a folder by graphical interface, you can start the termial from there using [this instruction](http://superuser.com/a/340051/276588).

...

Windows 10
----------

...

OS X 10
-------

...


Testing the "restest" database
##############################

Afer the "plug and play" installation instructions above, you can use the browser (or `wget` at terminal) to **functional tests**, without tokens or authetications. Enumerating tests to identify respective results:

 1. http://localhost:3000/t returns a JSON with the table `t` that we created above, at *Preparing a "restest" database* section.
 2. http://localhost:3000/t?select=note&label=eq.b  returns a JSON with the result of `SELECT note FROM t WHERE label='b'`.
 3. ...

The JSON results:

```json
##  test-1:
[
 {"id":1,"label":"first","note":"the first","created":"2017-02-19"},
 {"id":2,"label":"second","note":"the 2nd","created":"2017-02-19"},
 {"id":3,"label":"a","note":null,"created":"2017-02-19"},
 {"id":4,"label":"b","note":"last","created":"2017-02-19"}
]

##  test-2:
[{"note":"last"}]

## test ...
...

```

