Providing images for <img>
==========================

:author: `pkel <https://github.com/pkel>`_

In this tutorial, you will learn how to create an endpoint for providing images to HTMl :code:<img> tags without client side javascript:

.. code-block:: html

   <img src="http://your.host/api/images?select=blob&id=eq.42" alt="Cute Kittens"/>

A browser encountering this this tag will send a request to your API.
It will set the :code:`Accept` header to something like :code:`image/png,image/svg+xml,image/*;q=0.8,*/*;q=0.5`, indicating that it prefers PNGs and SVGs over other media types.
We observe, that the wildcard media type :code:`image/*` is present independent of the browser.

PostgREST can return binary data from :code:`bytea` columns.
Per default, this happens only if the clients sends the :code:`Accept: application/octet-stream` header.
As you see, the browser's image request does not line up with the required media type.
Luckily, since version 6, we can configure additional binary media types.
After adding

.. code-block:: bash

   raw-media-types='image/*'

to the PostgREST configuration, we only have to create an appropriate endpoint:

.. code-block:: postgres

   create table public.images(
     id   int primary key
   , blob bytea
   );

In principle, you are ready to go with this minimum configuration.

Response headers
----------------

The above configuration has some problems:

- The served images will not be cached.
  This imposes stress on your database.
- The return content type is the first one given in the :code:`Accept` header.
  In the above example it would be `image/png`, even when you return a JPG file.
  This will confuse users when using the *Save image as* feature of their browser.
- The browser will derive a filename from the request URL.
  This will likely go wrong and confuse users.

We can address these problems by setting custom response headers.
This is only possible from within stored procedures, so we have to adapt our schema a little bit.

.. code-block:: postgres

   set search_path=public

   create table images(
     id   int primary key
   , name text
   , type text
   , blob bytea
   );

   create or replace function image(id int) returns bytea as
   $$
     declare headers text;
     begin
       select format('[{"Content-Type": "%s"}, {"Content-Disposition": "attachment, filename=\"%s\""}, {"Cache-Control": "max-age=259200"}]', i.type, i.name)
         from images as i where i.id = image.id into headers;
       perform set_config('response.headers', headers, true);
       return(select blob from images as i where i.id = image.id);
     end
   $$ language plpgsql;

We also adapt the HTML snippet:

.. code-block:: html

   <img src="http://your.host/api/rpc/image?id=42" alt="Cute Kittens"/>

To Do
-----

- Return 404 when id is not present in table.
  How can we do it?
- If we could trigger raw output via a config parameter from within the procedure, we could provide a generic file endpoint.
