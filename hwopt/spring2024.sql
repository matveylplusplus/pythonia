PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE classes (
    class_name TEXT PRIMARY KEY,
    class_state TEXT NOT NULL CHECK (
        class_state == 'm'
        OR class_state == 'g'
    ),
    total_class_points INTEGER NOT NULL CHECK (total_class_points > 0)
);
INSERT INTO classes VALUES('cmsc351','m',600);
INSERT INTO classes VALUES('stat410','m',100);
INSERT INTO classes VALUES('cmsc330','m',100);
CREATE TABLE IF NOT EXISTS "lp_template_phases" (
    late_policy_name TEXT,
    phase_value REAL CHECK (
        0 < phase_value
        AND phase_value <= 1
    ),
    deadline_variable TEXT,
    hour_offset INT,
    PRIMARY KEY (late_policy_name, deadline_variable, hour_offset)
);
INSERT INTO lp_template_phases VALUES('stand',1.0,'x1',0);
INSERT INTO lp_template_phases VALUES('1x10',0.10000000000000000555,'x1',0);
INSERT INTO lp_template_phases VALUES('1x10',0.9000000000000000222,'x1',24);
INSERT INTO lp_template_phases VALUES('psyc100endsem',0.050000000000000002775,'x1',0);
INSERT INTO lp_template_phases VALUES('psyc100endsem',0.94999999999999995559,'x2',0);
INSERT INTO lp_template_phases VALUES('3x5',0.050000000000000002775,'x1',0);
INSERT INTO lp_template_phases VALUES('3x5',0.050000000000000002775,'x1',24);
INSERT INTO lp_template_phases VALUES('3x5',0.050000000000000002775,'x1',48);
INSERT INTO lp_template_phases VALUES('3x5',0.84999999999999997779,'x1',72);
CREATE TABLE assignment_templates (
    template_name TEXT PRIMARY KEY,
    class_name TEXT,
    pct_value REAL CHECK (
        0 < pct_value
        AND pct_value <= 1
    ),
    late_policy_name TEXT,
    FOREIGN KEY (late_policy_name) REFERENCES "lp_template_phases" (late_policy_name) ON UPDATE CASCADE,
    FOREIGN KEY (class_name) REFERENCES classes (class_name) ON UPDATE CASCADE
);
CREATE TABLE test (realnum REAL);
INSERT INTO test VALUES(0.018181818181818198282);
INSERT INTO test VALUES(0.018181818181818184404);
INSERT INTO test VALUES(1.8181818181818198976);
INSERT INTO test VALUES(3.5650623885917997156e-05);
INSERT INTO test VALUES(1.3986013986013999892e-05);
INSERT INTO test VALUES(0.0);
INSERT INTO test VALUES(1.3986013986013999892e-05);
INSERT INTO test VALUES(0.0);
INSERT INTO test VALUES(0.0);
INSERT INTO test VALUES(1.398601398601398634e-05);
CREATE TABLE test2 (num1 INT, num2 INT);
INSERT INTO test2 VALUES(1,0);
INSERT INTO test2 VALUES(1,1);
INSERT INTO test2 VALUES(1,2);
COMMIT;
