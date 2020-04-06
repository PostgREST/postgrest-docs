Upcoming
========

These are changes yet unreleased. If you'd like to try them out before a
new official release, you can `build_source`.

Added
-----

-   Support for the `on_conflict <on_conflict>` query parameter to
    UPSERT based on a unique constraint. --
    [@ykst](https://github.com/ykst)

-   Support for `planned_count` and `estimated_count`. --
    [@steve-chavez](https://github.com/steve-chavez)

-   Support for `Resource Embedding Disambiguation <embed_disamb>`. --
    [@steve-chavez](https://github.com/steve-chavez)

-   Support for user defined socket permission via
    `server-unix-socket-mode` config option --
    [@Dansvidania](https://github.com/Dansvidania)

-   HTTP logic improvements --
    [@steve-chavez](https://github.com/steve-chavez)

    > -   Support for HTTP HEAD requests.
    > -   GUCs for `guc_req_path_method`.
    > -   Support for `pre_req_headers`.
    > -   Allow overriding provided headers(Content-Type, Location, etc)
    >     by `guc_resp_hdrs`
    > -   Access to the `Authorization` header value through
    >     `request.header.authorization`

-   Documentation improvements

    -   Reference for `s_proc_embed`.
    -   Reference for `mutation_embed`.
    -   Reference for filters on `json_columns`.

Fixed
-----

-   Allow embedding a VIEW when its source table foreign key is UNIQUE
    -- [@bwbroersma](https://github.com/bwbroersma)
-   `Accept: application/vnd.pgrst.object+json` behavior is now enforced
    for POST/PATCH/DELETE regardless of `Prefer: return=minimal` --
    [@dwagin](https://github.com/dwagin)
-   Fix self join resource embedding on PATCH --
    [@herulume](https://github.com/herulume),
    [@steve-chavez](https://github.com/steve-chavez)
-   Allow PATCH/DELETE without `Prefer: return=minimal` on tables with
    no SELECT privileges --
    [@steve-chavez](https://github.com/steve-chavez)
-   Fix many to many resource embedding for RPC/PATCH --
    [@steve-chavez](https://github.com/steve-chavez)

Changed
-------

-   `bulk_call` should now be done by specifying a
    `Prefer: params=multiple-objects` header.
-   Resource Embedding now outputs an error when multiple relationships
    between two tables are found, see `embed_disamb`.
-   `server-proxy-uri` config option has been renamed to
    `openapi-server-proxy-uri`.
-   Default Unix Socket file mode from 755 to 660
