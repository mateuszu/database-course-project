CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE TABLE IF NOT EXISTS Employee(
    id              integer primary key,
    superior        integer default NULL,
    data            text default NULL,
    admin           integer,
    password        text default NULL
);

GRANT SELECT,INSERT,UPDATE,DELETE ON ALL TABLES IN SCHEMA public TO app;

