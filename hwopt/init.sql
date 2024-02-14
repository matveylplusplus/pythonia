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
    deadline TEXT,
    deadline_offset INT,
    PRIMARY KEY (policy_name, deadline, deadline_offset)
);
CREATE TABLE IF NOT EXISTS assignment_templates (
    template_name TEXT PRIMARY KEY,
    class_name TEXT,
    pct_value REAL CHECK (
        0 < pct_value
        AND pct_value <= 1
    ),
    late_policy_name TEXT,
    FOREIGN KEY (late_policy_name) REFERENCES late_phases (policy_name) ON UPDATE CASCADE,
    FOREIGN KEY (class_name) REFERENCES classes (class_name) ON UPDATE CASCADE
);