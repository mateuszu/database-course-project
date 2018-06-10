create table if not exists Employee(
    id              serial primary key,
    admin           integer default null,
    passwd          text default null,
    data            text,
    newpasswd       text,
    emp1            integer default null,
    emp             integer
);


