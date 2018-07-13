CREATE TABLE process
(
    id INTEGER NOT NULL PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(128) NOT NULL,
    status_id INTEGER,
    start_time TIMESTAMP,
    end_time DATETIME,
    last_active_time DATETIME,
    process_ratio INTEGER
);
CREATE TABLE event_log
(
    id INTEGER NOT NULL PRIMARY KEY AUTO_INCREMENT,
    event VARCHAR(128) NOT NULL,
    detail TEXT
)