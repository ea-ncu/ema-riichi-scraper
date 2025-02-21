create table tournaments(
    id serial primary key,
    number int unique not null,
    name text not null,
    place text,
    country text,
    date date not null,
    players int,
    mers text,
    rules text
);

create table players(
    id serial primary key,
    ema_id text unique,
    first_name text,
    last_name text,
    country text
);

create table tournament_results(
    tournament_id int not null,
    player_id int not null,
    score decimal(10),
    primary key (tournament_id, player_id),
    foreign key (tournament_id) references tournaments(id) on delete cascade,
    foreign key (player_id) references players(id) on delete cascade
)