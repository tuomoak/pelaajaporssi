CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
    );

CREATE TABLE players (
    id INTEGER PRIMARY KEY,
    NAME TEXT,
    PROFILE TEXT,
    user_id INTEGER References users
    );


CREATE TABLE roles (
    id INTEGER PRIMARY KEY,
    title TEXT,
    value TEXT
    );

CREATE TABLE player_roles (
    player_id INTEGER,
    role_type TEXT,
    role_name TEXT,
    role_value DEFAULT 0 NOT NULL,
    FOREIGN KEY (player_id) REFERENCES players(id)
    );

CREATE TABLE classes (
    id INTEGER PRIMARY KEY,
    title TEXT,
    value TEXT
    );

CREATE TABLE player_classes (
    player_id INTEGER,
    title TEXT,
    value TEXT,
    FOREIGN KEY (player_id) REFERENCES players(id)
    );

CREATE TABLE ideas (
    id INTEGER PRIMARY KEY,
    title TEXT,
    value TEXT
    );

 CREATE TABLE contacts (
    id INTEGER PRIMARY KEY,
    title TEXT,
    value TEXT
    );

CREATE TABLE player_ideas (
    id INTEGER PRIMARY KEY,
    title TEXT,
    value TEXT,
    contact_type TEXT,
    player_id INTEGER References players,
    user_id INTEGER References users
    );