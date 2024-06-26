-------------------------------------------------
-- drop table if exists fish;
-- create table fish (
--     id integer PRIMARY KEY AUTOINCREMENT,
--     identity varchar(64) NOT NULL,
--     type varchar(16) NOT NULL,
--     byte_count integer NOT NULL,
--     preview blob DEFAULT NULL,
--     description text NOT NULL DEFAULT '',
--     tags varchar(128) NOT NULL DEFAULT '',
--     is_marked tinyint NOT NUll DEFAULT 0,
--     is_locked tinyint NOT NUll DEFAULT 0,
--     extra_info text NOT NULL DEFAULT '{}',
--     create_time DATETIME NOT NULL DEFAULT(datetime(CURRENT_TIMESTAMP, 'localtime')),
--     update_time DATETIME NOT NULL DEFAULT(datetime(CURRENT_TIMESTAMP, 'localtime')),
--     CONSTRAINT unique_data UNIQUE (identity)
-- );

-- create index index_time on fish (update_time);

-- drop TRIGGER if exists update_fish;
-- CREATE TRIGGER update_fish
-- AFTER UPDATE ON fish
-- FOR EACH ROW
-- BEGIN
--     UPDATE fish SET update_time = datetime(CURRENT_TIMESTAMP, 'localtime') WHERE id = NEW.id;
-- END;

-- drop table if exists request;
-- create table request (
--     id integer PRIMARY KEY AUTOINCREMENT,
--     request_id varchar(64),
--     url varchar(64),
--     time_cost text,
--     origin_input text,
--     real_input text,
--     response text,
--     extra_info text,
--     create_time DATETIME NOT NULL DEFAULT(datetime(CURRENT_TIMESTAMP, 'localtime'))
-- );
-------------------------------------------------

-- delete from request;
-- select * from request order by create_time desc limit 20;

SELECT strftime('%Y-%m-%d', create_time) AS date,
       COUNT(*) AS record_count
FROM request
GROUP BY strftime('%Y-%m-%d', create_time)
ORDER BY date;