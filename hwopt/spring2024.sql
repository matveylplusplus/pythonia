PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE major_maps (
    major_state TEXT PRIMARY KEY CHECK (
        major_state == 'm'
        OR major_state == 'g'
    ),
    major_factor REAL NOT NULL CHECK (
        0 < major_factor
        AND major_factor <= 1
    )
);
INSERT INTO major_maps VALUES('g',0.625);
INSERT INTO major_maps VALUES('m',1.0);
CREATE TABLE classes (
    class_name TEXT PRIMARY KEY,
    major_state TEXT NOT NULL,
    total_class_points INTEGER NOT NULL CHECK (total_class_points > 0),
    FOREIGN KEY (major_state) REFERENCES major_maps (major_state) ON UPDATE CASCADE
);
CREATE TABLE lp_templates (late_policy_name TEXT PRIMARY KEY);
CREATE TABLE lp_template_deadvars (
    late_policy_name TEXT,
    deadline_variable TEXT,
    FOREIGN KEY (late_policy_name) REFERENCES lp_templates (late_policy_name) ON UPDATE CASCADE,
    PRIMARY KEY (late_policy_name, deadline_variable)
);
CREATE TABLE lp_template_deadvar_phases (
    late_policy_name TEXT,
    phase_value REAL CHECK (
        0 < phase_value
        AND phase_value <= 1
    ),
    deadline_variable TEXT,
    hour_offset INT,
    FOREIGN KEY (late_policy_name, deadline_variable) REFERENCES lp_template_deadvars (late_policy_name, deadline_variable) ON UPDATE CASCADE,
    PRIMARY KEY (late_policy_name, deadline_variable, hour_offset)
);
CREATE TABLE assignment_templates (
    template_name TEXT PRIMARY KEY,
    class_name TEXT,
    points REAL,
    late_policy_name TEXT,
    FOREIGN KEY (class_name) REFERENCES classes (class_name) ON UPDATE CASCADE,
    FOREIGN KEY (late_policy_name) REFERENCES lp_templates (late_policy_name) ON UPDATE CASCADE
);
CREATE TABLE assignments (
    assignment_name TEXT PRIMARY KEY,
    class_name TEXT,
    points REAL,
    late_policy_name TEXT,
    FOREIGN KEY (class_name) REFERENCES classes (class_name) ON UPDATE CASCADE,
    FOREIGN KEY (late_policy_name) REFERENCES lp_templates (late_policy_name) ON UPDATE CASCADE
);
CREATE TABLE deadvar_maps (
    assignment_name TEXT,
    late_policy_name TEXT,
    deadline_variable TEXT,
    deadline_instance TEXT NOT NULL,
    FOREIGN KEY (assignment_name) REFERENCES assignments (assignment_name) ON UPDATE CASCADE,
    FOREIGN KEY (late_policy_name, deadline_variable) REFERENCES lp_template_deadvars (late_policy_name, deadline_variable) ON UPDATE CASCADE,
    PRIMARY KEY (
        assignment_name,
        late_policy_name,
        deadline_variable
    )
);
COMMIT;
