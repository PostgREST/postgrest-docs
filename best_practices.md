Function privileges
===================

By default, when a function is created, the right to execute it is is
not restricted by role, but this probably isn't consistent with best
practices for an API design. If you want functions to be executable
exclusively by a given role upon their creation, issue psql instructions
similar to this:

    -- To stop functions from being universally executable upon creation (note the IN SCHEMA part).
    ALTER DEFAULT PRIVILEGES IN SCHEMA api REVOKE EXECUTE ON FUNCTIONS FROM PUBLIC;
    -- To grant execution rights for functions to a specific role upon function creation.
    ALTER DEFAULT PRIVILEGES IN SCHEMA api GRANT EXECUTE ON FUNCTIONS TO my_role;

See [PostgreSQL alter default
privileges](https://www.postgresql.org/docs/current/static/sql-alterdefaultprivileges.html)
for more details.

The foregoing example may not be appropriate in all situations. For
instance you may have a situation where different functions are intended
to be called by different roles. In that case you will <span
class="title-ref">not</span> want to grant <span
class="title-ref">EXECUTE</span> to one specific role by default.
Instead you will want to manually grant executability on a case by case
basis.

By default, a function is executed with the privileges of the user who
calls it. This means that the user has to have all permissions to do the
operations the procedure performs.

Another option is to define the function with the `SECURITY DEFINER`
option. Then only one permission check will take place, the permission
to call the function, and the operations in the function will have the
authority of the user who owns the function itself. See [PostgreSQL
documentation](https://www.postgresql.org/docs/current/static/sql-createfunction.html#SQL-CREATEFUNCTION-SECURITY)
for more details.
