CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE TABLE IF NOT EXISTS Employee(
    id              serial PRIMARY KEY,
    admin           integer default NULL,
    passwd          text default NULL,
    data            text NOT NULL,
    newpasswd       text,
    emp1            integer default NULL,
    emp             integer
);

GRANT SELECT,INSERT,UPDATE,DELETE ON ALL TABLES IN SCHEMA public TO app;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO app;

