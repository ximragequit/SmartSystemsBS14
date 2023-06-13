DROP TABLE IF EXISTS sensor;
DROP TABLE IF EXISTS reading;
DROP TABLE IF EXISTS fan_stats;
DROP TABLE IF EXISTS vent_stats;
DROP TABLE IF EXISTS events;
DROP TABLE IF EXISTS logging;

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
    zeit VARCHAR(10),
    PRIMARY KEY (reading_id)
);

CREATE TABLE vent (
    vent_id SMALLINT NOT NULL,
    vent_description VARCHAR(50),
    vent_location VARCHAR(50),
    PRIMARY KEY (vent_id)
);

CREATE TABLE vent_stats (
    vent_stat_id SMALLINT NOT NULL,
    vent_id SMALLINT,
    FOREIGN KEY (vent_id) REFERENCES vent(vent_id),
    vent_status FLOAT,
    zeit VARCHAR(10),
    PRIMARY KEY (vent_stat_id)
);


CREATE TABLE events (
    event_id SMALLINT NOT NULL,
    zeit VARCHAR(10),
    reading_id SMALLINT,
    FOREIGN KEY (reading_id) REFERENCES reading(reading_id),
    vent_stat_id SMALLINT,
    FOREIGN KEY (vent_stat_id) REFERENCES vent_stats(vent_stat_id),
    trigger_temperature FLOAT,
    PRIMARY KEY (event_id)
);


-- CREATE TABLE logging (
--     log_id SMALLINT NOT NULL,
--     event_id SMALLINT,
--     FOREIGN KEY (event_id) REFERENCES events(event_id),
--     temperature FLOAT,
--     zeit TIME,
--     PRIMARY KEY (log_id)
-- );


-- Fill in data

INSERT INTO sensor VALUES
(1,'Temperatur Sensor','main'),
(2,'Zusatz Temperatur Sensor', 'back');

INSERT INTO vent VALUES
(1,'Ventilator','main');

INSERT INTO reading VALUES
(1,1,00.00,'00:00:00');

INSERT INTO vent_stats VALUES
(1,1,0,'00:00:00');
