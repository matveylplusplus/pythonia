CREATE TABLE current_time_example (
    time_id bigserial,
    current_timestamp_col timestamp with time zone,
    clock_timestamp_col timestamp with time zone
);
INSERT INTO current_time_example (current_timestamp_col)
SELECT current_timestamp
FROM generate_series (1, 1000);
SELECT *
FROM current_time_example;