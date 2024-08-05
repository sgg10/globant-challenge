--liquibase formatted sql

--changeset sebastian.granda:1
--comment: Insert data parameterized into tables

-- insert data parameterized task_type table
INSERT INTO task_type (name, changelog_id) VALUES ('LOAD', 1);
INSERT INTO task_type (name, changelog_id) VALUES ('BACKUP', 1);
INSERT INTO task_type (name, changelog_id) VALUES ('RESTORE', 1);
INSERT INTO task_type (name, changelog_id) VALUES ('REPORT', 1);
INSERT INTO task_type (name, changelog_id) VALUES ('MIGRATION', 1);

-- insert data parameterized task_status table
INSERT INTO task_status (name, changelog_id) VALUES ('PENDING', 1);
INSERT INTO task_status (name, changelog_id) VALUES ('IN_PROGRESS', 1);
INSERT INTO task_status (name, changelog_id) VALUES ('COMPLETED', 1);
INSERT INTO task_status (name, changelog_id) VALUES ('FAILED', 1);
