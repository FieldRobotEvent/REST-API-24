CREATE TABLE IF NOT EXISTS timer
(
    id SERIAL PRIMARY KEY,
    group_name TEXT NOT NULL,
    task_name TEXT NOT NULL,
    running BOOLEAN NOT NULL,
    timestamp timestamp default current_timestamp
);