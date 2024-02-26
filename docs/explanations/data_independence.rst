.. _data_independence:

Data Independence
#################

  "Data independence means we have the freedom to change the physical database without changing the logical database and therefore all your investment in existing applications, existing retrieval requests, existing people, existing training, existing database designs; all of that is still good. Data independence translates into protecting the users investment."

  -- C.J. Date

Data Independence in PostgreSQL can be achieved by hiding tables from users and only exposing them views. PostgREST also proposes an additional way by using :ref:`domain_reps`.
