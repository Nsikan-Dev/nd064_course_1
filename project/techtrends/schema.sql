DROP TABLE IF EXISTS posts;

CREATE TABLE posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    title TEXT NOT NULL,
    content TEXT NOT NULL
);

CREATE TABLE db_connections (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    connection_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);