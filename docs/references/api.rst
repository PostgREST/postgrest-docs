.. _api:

API
###

PostgREST exposes three database objects of a schema as resources: tables, views and stored procedures.

.. toctree::
   :glob:
   :maxdepth: 1

   api/tables_views.rst
   api/stored_procedures.rst
   api/schemas.rst
   api/resource_embedding.rst
   api/openapi.rst
   api/resource_representation.rst
   api/*

.. raw:: html

  <script type="text/javascript">
  switch (window.location.hash) {
    case '#custom-queries':
      console.log('Redirecting to custom queries...');
      window.location.href = "api/url_grammar.html#custom-queries"
      break;
    default:
      console.log(`Nothing to do`);
  }
  </script>