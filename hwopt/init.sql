CREATE TABLE IF NOT EXISTS major_maps (
    major_state TEXT PRIMARY KEY CHECK (
        major_state == 'm'
        OR major_state == 'g'
    ),
    major_factor REAL NOT NULL CHECK (
        0 < major_factor
        AND major_factor <= 1
    )
);
CREATE TABLE IF NOT EXISTS classes (
    class_name TEXT PRIMARY KEY,
    major_state TEXT,
    total_class_points INTEGER NOT NULL CHECK (total_points > 0),
    FOREIGN KEY (major_state) REFERENCES major_maps (major_state) ON UPDATE CASCADE
);
CREATE TABLE IF NOT EXISTS lp_templates (late_policy_name TEXT PRIMARY KEY);
CREATE TABLE IF NOT EXISTS lp_template_phases (
    late_policy_name TEXT,
    phase_value REAL CHECK (
        0 < phase_value
        AND phase_value <= 1
    ),
    deadline_variable TEXT,
    hour_offset INT,
    FOREIGN KEY (late_policy_name) REFERENCES lp_templates (late_policy_name) ON UPDATE CASCADE,
    PRIMARY KEY (late_policy_name, deadline_variable, hour_offset)
);
CREATE TABLE IF NOT EXISTS assignment_templates (
    template_name TEXT PRIMARY KEY,
    class_name TEXT,
    points REAL CHECK (
        0 < points
        AND points <= 1
    ),
    late_policy_name TEXT,
    FOREIGN KEY (late_policy_name) REFERENCES lp_templates (late_policy_name) ON UPDATE CASCADE,
    FOREIGN KEY (class_name) REFERENCES classes (class_name) ON UPDATE CASCADE
);
CREATE TABLE deadvar_maps IF NOT EXISTS (
    assignment_name TEXT,
    deadline_variable TEXT,
    deadline_instance TEXT NOT NULL,
    FOREIGN KEY (assignment_name) REFERENCES assignments (assignment_name) ON UPDATE CASCADE,
    FOREIGN KEY (deadline_variable) REFERENCES lp_template_phases (deadline_variable) ON UPDATE CASCADE,
    PRIMARY KEY (assignment_name, deadline_variable)
);
INSERT INTO major_maps
VALUES ('g', DECIMAL(5.0 / 8)),
    ('m', 1.0);