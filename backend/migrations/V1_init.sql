DROP TABLE IF EXISTS users;

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    status BOOLEAN,
    token VARCHAR(50) UNIQUE
);

TRUNCATE users;

CREATE INDEX token_idx ON users (token);
