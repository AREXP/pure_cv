DROP TABLE IF EXISTS users;

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    status BOOLEAN NOT NULL,
    token VARCHAR(50) UNIQUE NOT NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL
);

TRUNCATE users;

CREATE INDEX token_idx ON users (token);
