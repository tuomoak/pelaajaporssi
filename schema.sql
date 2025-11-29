CREATE TABLE players (
    id INTEGER PRIMARY KEY,
    NAME TEXT,
    PROFILE TEXT,
    user_id INTEGER References users
    );


CREATE TABLE player_def_roles (
    player_id INTEGER,
    role_name_eng TEXT,
    role_name_fi TEXT,
    role_value DEFAULT 0 NOT NULL,
    FOREIGN KEY (player_id) REFERENCES players(id)
    );

CREATE TABLE player_bat_roles (
    player_id INTEGER,
    role_name_eng TEXT,
    role_name_fi TEXT,
    role_value DEFAULT 0 NOT NULL,
    FOREIGN KEY (player_id) REFERENCES players(id)
    );

CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
);



       
 
