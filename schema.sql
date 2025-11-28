CREATE TABLE players (
    id INTEGER PRIMARY KEY,
    NAME TEXT,
    PROFILE TEXT,
    pitcher BIT  DEFAULT 0 NOT NULL,
    frontfield BIT  DEFAULT 0 NOT NULL,
    midfield BIT  DEFAULT 0 NOT NULL,
    baseman BIT  DEFAULT 0 NOT NULL,   
    outfielder BIT  DEFAULT 0 NOT NULL,  
    runner BIT  DEFAULT 0 NOT NULL,    
    advancehitter BIT  DEFAULT 0 NOT NULL,  
    runhitter BIT  DEFAULT 0 NOT NULL,  
    flyhitter BIT  DEFAULT 0 NOT NULL,
    joker BIT  DEFAULT 0 NOT NULL 
    );



CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
);
       
 
