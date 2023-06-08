DROP TABLE IF EXISTS sensor;
DROP TABLE IF EXISTS reading;
DROP TABLE IF EXISTS fan_stats;
DROP TABLE IF EXISTS vent_stats;
DROP TABLE IF EXISTS events;
DROP TABLE IF EXISTS log;

CREATE TABLE sensor (
    sensor_id SMALLINT NOT NULL,
    sensor_description VARCHAR(50),
    sensor_location VARCHAR(50),
    PRIMARY KEY (sensor_id)
);


CREATE TABLE reading (
    reading_id SMALLINT NOT NULL,
    sensor_id SMALLINT,
    FOREIGN KEY (sensor_id) REFERENCES sensor(sensor_id),
    temperature FLOAT,
    zeit TIME,
    PRIMARY KEY (reading_id)
);


CREATE TABLE fan_stats (
    fan_id SMALLINT NOT NULL,
    fan_description VARCHAR(50),
    fan_location VARCHAR(50),
    fan_status FLOAT,
    zeit TIME,
    PRIMARY KEY (fan_id)
);


CREATE TABLE vent_stats (
    vent_id SMALLINT NOT NULL,
    vent_description VARCHAR(50),
    vent_location VARCHAR(50),
    vent_status FLOAT,
    zeit TIME,
    PRIMARY KEY (vent_id)
); 


CREATE TABLE events (
    event_id SMALLINT NOT NULL,
    reading_id SMALLINT,
    FOREIGN KEY (reading_id) REFERENCES reading(reading_id),
    fan_id SMALLINT,
    FOREIGN KEY (fan_id) REFERENCES fan_stats(fan_id),
    vent_id SMALLINT,
    FOREIGN KEY (vent_id) REFERENCES vent_stats(vent_id),
    trigger_temperature FLOAT,
    PRIMARY KEY (event_id)
);


CREATE TABLE log (
    log_id SMALLINT NOT NULL,
    event_id SMALLINT,
    FOREIGN KEY (event_id) REFERENCES events(event_id),
    temperature FLOAT,
    zeit TIME,
    PRIMARY KEY (log_id)
);
