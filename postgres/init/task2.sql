CREATE TABLE IF NOT EXISTS task2
(
    id SERIAL PRIMARY KEY,
    group_name TEXT NOT NULL,
    row_count INT NOT NULL,
    plant_count INT NOT NULL,
    timestamp timestamp default current_timestamp
);