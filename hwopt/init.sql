CREATE TABLE IF NOT EXISTS classes (
    class_name TEXT PRIMARY KEY,
    major_or_gened TEXT NOT NULL CHECK (
        major_or_gened == 'm'
        OR major_or_gened == 'g'
    ),
    total_points INTEGER NOT NULL CHECK (total_points > 0)
);
CREATE TABLE IF NOT EXISTS late_phases (
    policy_name TEXT,
    pct_value REAL CHECK (
        0 < pct_value
        AND pct_value <= 1
    ),
    deadline_scheme TEXT,
    PRIMARY KEY (policy_name, deadline_scheme)
);