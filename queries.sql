CREATE TABLE IF NOT EXISTS Employee(
    id              serial PRIMARY KEY,
    admin           integer default NULL,
    passwd          text default NULL,
    data            text NOT NULL,
    newpasswd       text,
    emp1            integer default NULL,
    emp             integer
);


