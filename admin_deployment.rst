Deployment
----------

Heroku
~~~~~~

Account setup on Heroku
^^^^^^^^^^^^^^^^^^^^^^^

Setting up a simple Heroku “Free Account” is easy and should take no
more than a couple of minutes. For this guide I will be using a
fictitious email account “postgrest@kismail.ru” to set up the account on
Heroku. You can use whatever email account you desire. NOTE: During
signup you will be asked to “Pick your primary development language”. It
is safe here to choose any language or simply “I use another language”.

1. Heroku signup input |Heroku signup input|
2. Heroku signup waiting |Heroku signup waiting|
3. Heroku signup confirmation |Heroku signup confirmation|
4. Heroku signup password |Heroku signup password|
5. Heroku signup success |Heroku signup success|

After initial signup, you will receive a confirmation email. You have to
open the link provided in the email to activate your Heroku Free
Account.

New “App” setup in Heroku
^^^^^^^^^^^^^^^^^^^^^^^^^

Creating an “App” can be seen as creating an environment, complete with
hardware resources, to run any code you wish. It is here that the
PostgreSQL database and the PostgREST instance will reside.

Select “New App” and then select a new name for the “App”. It can be
anything as long as it is available. The “Run-time Selection” region can
be anywhere, it only specifies where the app data is stored.

1. Heroku initial empty page |Heroku initial empty page|
2. Heroku create new app |Heroku create new app|
3. Heroku app creation success |Heroku app creation success|

Setup of PostgreSQL add-on in newly setup “App”
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

At this point you should have your new “App” environment setup and
running. It is now time to add a PostgreSQL database to your “App”. In
your “App” screen, you will have several tabs with names such as
“Overview”, “Resources”, “Deploy”, etc.

1. Choose “Resources”. This will show you the resources currently
   running in your “App”, which should be empty as you have yet to
   deploy any resources.
2. On the “Resources” page, under the header “Add-ons” you will find a
   search bar. Type in “PostgreSQL”, which will show you “Heroku
   PostgreSQL”. Click on the name to show a deployment dialog. |Heroku
   find postgresql db| |Heroku install postgresql db|
3. After deployment, you will see a line in your “Add-ons” named “Heroku
   PostgreSQL”. You have now added a PostgreSQL database to your “App”.
   Now to setup the database. NOTE: It might take a few minutes for
   Heroku to initialize the db, so please wait 1-2 minutes before moving
   on to step 4. |Heroku installed postgresql db|
4. Click on the newly added “Heroku PostgreSQL” in your “Add-ons” and
   you will be taken to the database “Overview” page. Here you will find
   all the information necessary to find and connect to your PostgreSQL
   DB. This information will be very important when setting up
   PostgREST. |Heroku db panel| |Heroku db overview| |Heroku db stats|
   |Heroku db success|
5. At this point, you have full access to the PostgreSQL database and
   can create tables, schemas, functions, etc. NOTE: The PostgREST setup
   will only work against a single Schema. This means that tables
   outside of the selected Schema will not be directly accessible via
   API calls.

Testing of newly setup PostgreSQL
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Before we move on to deploying PostgREST, we could perform a quick test
to see that our DB is up and running. This can be done in many different
ways, one of which is the `pgAdmin
GUI <http://agileforce.co.uk/heroku-workshop/heroku-postgres/pgadmin.html>`__.
It is also possible to connect with psql for simple testing.

NOTE: When using pgAdmin to connect to the DB, you will see many other
inaccessible DBs. Don’t be alarmed. Find your DB by the “Database“ name
provided in the Overview.

Setup of PostgREST deployment
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Now it is time to deploy PostgREST. The PostgREST deployment on Heroku
is not an “Add-on”, it is an “Element”. It can be found by opening the
menu at the top right of the Heroku screen and selecting “Elements”.
Search for “PostgREST” and find it under “Buttons”. Opening the
“PostgREST” page, a “Deploy to Heroku” button will be present on the
page. This button will lead to the initial setup and configuration page
for the PostgREST deployment on your “App”.

1. Heroku find PostgREST 1 |Heroku find Postgrest 1|
2. Heroku find PostgREST 2 |Heroku find Postgrest 2|
3. Heroku PostgREST page |Heroku PostgREST page|
4. Heroku PostgREST install |Heroku PostgREST install|

Explanations for each field in the PostgREST setup page:

-  **App Name** (optional) : The name chosen for the PostgREST
   deployment. NOTE: The name you choose will be the beginning of your
   specific API url. So if you choose “bugbunny”, your API url will be
   “bugbunny.herokuapp.com”.
-  **Run-time Selection** : Simply select the region the deployment
   (basically data) will be stored.
-  **BUILDPACK\_URL** : Do not change this. This points to the pack that
   will be used for setup, which cannot be changed if you want a
   functioning PostgREST.
-  **POSTGREST\_VER** : Do not change this. Version of PostgREST used
   for installation.

PostgREST configuration (Information from the PostgreSQL Overview page):

-  **DB\_NAME** : Here you must provide the name of the database you
   setup earlier, which can be found on the “Overview” page of the
   PostgreSQL add-on. It should be something like “d41vontrqmq2oo”.
-  **AUTH\_ROLE** : This is the role of an authenticated user. All
   authenticated calls to the API will use this user role when
   attempting to perform actions against the PostgreSQL database. User
   authentication is done using the procedure described on the `Security
   page </admin/security/>`__. :w For the purpose of this demo, you can
   simply input the data in the “User” field of the Overview page of the
   PostgreSQL add-on. It should be something like “nhvnhzryphzmcp”.
-  **AUTH\_PASS** : Simply the password for the authenticated user, also
   found on the Overview page of the PostgreSQL add-on. It should be
   something like “5YDLXynT2ZWqUA6c2c\_D12TofA”.
-  **ANONYMOUS\_ROLE** : This is the role for any unauthenticated call
   to the API. In a regular PostgreSQL database this role could be for
   calls that for example don’t alter data, but simply retrieve data.
   Unfortunately in Heroku Hobby-dev account, it is not possible to add
   any roles to your PostgreSQL database, which means you will have to
   use the only role provided when PostgreSQL is setup, the admin role.
   So input the same data provided in the “AUTH\_ROLE” field. Please
   keep in mind that this admin role has full access and can do
   anything, including deleting from the db.
-  **DB\_HOST** : This is the URL to the database, which should be
   copied directly from the Overview page of the PostgreSQL add-on.
-  **DB\_PORT** : The port to used when connecting to the database.
   Usually not necessary to change unless some specific manual changes
   have been made to the DB connection.
-  **DB\_POOL** : As the description states, “Maximum number of
   connections in database pool”. This parameter is not necessary to
   change.
-  **JWT\_SECRET** : Information regarding this parameter can be found
   in the `Security page </admin/security/>`__. For testing purposes,
   there is no need to change this parameter, but it is important to
   read and fully understand how JWT works if and when moving on from
   testing only.
-  **SCHEMA** : This parameter is very important when it comes to being
   able to access the information on the PostgreSQL DB via PostgREST, as
   it indicates what Schema on the DB should be made available through
   the API calls. Only a single Schema can be selected and the tables
   and views in that Schema will be accessible through the API, so
   please make sure that the correct Schema name is input here.

When all the above fields are filled in, the PostgREST configuration
should be ready for deployment. Pressing the “Deploy for free” button at
the bottom of the screen will initiate the deployment process, which
should take no more than a 1-2 minutes to finish. |Heroku PostgREST
installing| |Heroku PostgREST installed|

Testing the PostgREST deployment
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

At this point, you should have the PostgreSQL database and the PostgREST
Heroku element up and running. Time to test the setup. The easiest way
to see if things are up and running is to go to your “Personal Apps” in
your Heroku dashboard, select the name you selected when deploying
PostgREST (like “bugbunny”) and then pressing the “Open app” button at
the top, right corner of the screen. What should open is a new web page,
with a JSON representation of the tables in your PostgreSQL database.
(https://bugbunny.herokuapp.com/) |Heroku postgrest test 1|

An additional test to perform is to add the name of any table inside you
database Schema to the end of the PostgREST Heroku app URL, such as
https://bugbunny.herokuapp.com/people, where “people” is the name of the
Table in the database Schema. This will retrieve, in JSON form, all the
rows in the “People” table.

.. figure:: _static/img/heroku_guide/23_heroku_postgrest_test_2.png
   :alt: Heroku postgrest test 1

   Heroku postgrest test 1

Heroku LINKS:

-  `Heroku PostgreSQL
   Plans <https://devcenter.heroku.com/articles/heroku-postgres-plans>`__
-  `Heroku
   PostgREST <https://elements.heroku.com/buttons/begriffs/postgrest>`__

Debian
~~~~~~

(To be written)

.. |Heroku signup input| image:: _static/img/heroku_guide/1_heroku_signup_input.png
.. |Heroku signup waiting| image:: _static/img/heroku_guide/2_heroku_signup_waiting.png
.. |Heroku signup confirmation| image:: _static/img/heroku_guide/3_heroku_signup_confirmation.png
.. |Heroku signup password| image:: _static/img/heroku_guide/4_heroku_signup_password.png
.. |Heroku signup success| image:: _static/img/heroku_guide/5_heroku_signup_success.png
.. |Heroku initial empty page| image:: _static/img/heroku_guide/6_heroku_initial_empty_page.png
.. |Heroku create new app| image:: _static/img/heroku_guide/7_heroku_create_new_app.png
.. |Heroku app creation success| image:: _static/img/heroku_guide/8_heroku_app_created_success.png
.. |Heroku find postgresql db| image:: _static/img/heroku_guide/9_heroku_find_postgresql_db.png
.. |Heroku install postgresql db| image:: _static/img/heroku_guide/10_heroku_install_postgresql_db.png
.. |Heroku installed postgresql db| image:: _static/img/heroku_guide/11_heroku_installed_postgresql_db.png
.. |Heroku db panel| image:: _static/img/heroku_guide/12_heroku_db_panel.png
.. |Heroku db overview| image:: _static/img/heroku_guide/13_heroku_db_overview.png
.. |Heroku db stats| image:: _static/img/heroku_guide/14_heroku_db_stats.png
.. |Heroku db success| image:: _static/img/heroku_guide/15_heroku_app_with_db.png
.. |Heroku find Postgrest 1| image:: _static/img/heroku_guide/16_heroku_find_postgrest_1.png
.. |Heroku find Postgrest 2| image:: _static/img/heroku_guide/17_heroku_find_postgrest_2.png
.. |Heroku PostgREST page| image:: _static/img/heroku_guide/18_heroku_postgrest_page.png
.. |Heroku PostgREST install| image:: _static/img/heroku_guide/19_heroku_postgrest_installation.png
.. |Heroku PostgREST installing| image:: _static/img/heroku_guide/20_heroku_postgrest_installing.png
.. |Heroku PostgREST installed| image:: _static/img/heroku_guide/21_heroku_postgrest_installed.png
.. |Heroku postgrest test 1| image:: _static/img/heroku_guide/22_heroku_postgrest_test_1.png

