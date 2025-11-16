CREATE TABLE players (
    id INTEGER PRIMARY KEY,
    NAME TEXT,
    PROFILE TEXT,
    lukkari BIT  DEFAULT 0 NOT NULL,
    etukenttä BIT  DEFAULT 0 NOT NULL,
    polttolinja BIT  DEFAULT 0 NOT NULL,
    pesävahti BIT  DEFAULT 0 NOT NULL,   
    takakenttä BIT  DEFAULT 0 NOT NULL,  
    etenijä BIT  DEFAULT 0 NOT NULL,    
    vaihtaja BIT  DEFAULT 0 NOT NULL,  
    kotiuttaja BIT  DEFAULT 0 NOT NULL,  
    kopittaja BIT  DEFAULT 0 NOT NULL 
    );



CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
);
       
 
