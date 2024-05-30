CREATE TABLE IF NOT EXISTS task3
(
    id SERIAL PRIMARY KEY,
    group_name TEXT NOT NULL,
    x REAL NOT NULL,
    y REAL NOT NULL,
    final BOOLEAN NOT NULL,
    timestamp timestamp default current_timestamp
);