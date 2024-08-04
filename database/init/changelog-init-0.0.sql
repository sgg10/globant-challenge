--liquibase formatted sql

--changeset sebastian.granda:1
--comment: Create the initial tables for the database

-- CREATE TABLE department
CREATE TABLE IF NOT EXISTS department (
    id                  SERIAL NOT NULL,
    department          VARCHAR NOT NULL,
    changelog_id        INT NOT NULL DEFAULT -1,
    created_by_task_id  INT NOT NULL,
    created_at          TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at          TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT          department_pk PRIMARY KEY (id)
);
COMMENT ON TABLE department IS 'Stores information about the different departments within the organization';
COMMENT ON COLUMN department.id IS 'Unique identifier for each department, auto-incremented';
COMMENT ON COLUMN department.department IS 'Name of the department';
COMMENT ON COLUMN department.changelog_id IS 'Reference ID to track changes';
COMMENT ON COLUMN department.created_by_task_id IS 'ID of the task that created this record';
COMMENT ON COLUMN department.created_at IS 'Timestamp when the record was created';
COMMENT ON COLUMN department.updated_at IS 'Timestamp when the record was last updated';

-- CREATE TABLE job
CREATE TABLE IF NOT EXISTS job (
    id                  SERIAL NOT NULL,
    job                 VARCHAR NOT NULL,
    changelog_id        INT NOT NULL DEFAULT -1,
    created_by_task_id  INT NOT NULL,
    created_at          TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at          TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT          job_pk PRIMARY KEY (id)
);
COMMENT ON TABLE job IS 'Stores information about the different job roles within the organization';
COMMENT ON COLUMN job.id IS 'Unique identifier for each job, auto-incremented';
COMMENT ON COLUMN job.job IS 'Name of the job';
COMMENT ON COLUMN job.changelog_id IS 'Reference ID to track changes';
COMMENT ON COLUMN job.created_by_task_id IS 'ID of the task that created this record';
COMMENT ON COLUMN job.created_at IS 'Timestamp when the record was created';
COMMENT ON COLUMN job.updated_at IS 'Timestamp when the record was last updated';

-- CREATE TABLE employee
CREATE TABLE employee (
    id                  SERIAL PRIMARY KEY,
    name                VARCHAR NOT NULL,
    datetime            TIMESTAMP NOT NULL,
    department_id       INT NOT NULL,
    job_id              INT NOT NULL,
    changelog_id        INT NOT NULL DEFAULT -1,
    created_by_task_id  INT NOT NULL,
    created_at          TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at          TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
COMMENT ON TABLE employee IS 'Stores information about the employees within the organization';
COMMENT ON COLUMN employee.id IS 'Unique identifier for each employee, auto-incremented';
COMMENT ON COLUMN employee.name IS 'Name of the employee';
COMMENT ON COLUMN employee.datetime IS 'Date and time of hiring';
COMMENT ON COLUMN employee.department_id IS 'Foreign key referencing the department the employee belongs to';
COMMENT ON COLUMN employee.job_id IS 'Foreign key referencing the job role of the employee';
COMMENT ON COLUMN employee.changelog_id IS 'Reference ID to track changes';
COMMENT ON COLUMN employee.created_by_task_id IS 'ID of the task that created this record';
COMMENT ON COLUMN employee.created_at IS 'Timestamp when the record was created';
COMMENT ON COLUMN employee.updated_at IS 'Timestamp when the record was last updated';

-- CREATE TABLE task_type
CREATE TABLE task_type (
    id              SERIAL PRIMARY KEY,
    name            VARCHAR NOT NULL,
    changelog_id    INT NOT NULL DEFAULT -1,
    created_at      TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at      TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
COMMENT ON TABLE task_type IS 'Stores the different types of tasks that can be created and managed within the system';
COMMENT ON COLUMN task_type.id IS 'Unique identifier for each task type, auto-incremented';
COMMENT ON COLUMN task_type.name IS 'Name of the task type';
COMMENT ON COLUMN task_type.changelog_id IS 'Reference ID to track changes';
COMMENT ON COLUMN task_type.created_at IS 'Timestamp when the record was created';
COMMENT ON COLUMN task_type.updated_at IS 'Timestamp when the record was last updated';

-- CREATE TABLE task_status
CREATE TABLE task_status (
    id              SERIAL PRIMARY KEY,
    name            VARCHAR NOT NULL,
    changelog_id    INT NOT NULL DEFAULT -1,
    created_at      TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at      TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
COMMENT ON TABLE task_status IS 'Stores the different statuses that tasks can have';
COMMENT ON COLUMN task_status.id IS 'Unique identifier for each task status, auto-incremented';
COMMENT ON COLUMN task_status.name IS 'Name of the task status';
COMMENT ON COLUMN task_status.changelog_id IS 'Reference ID to track changes';
COMMENT ON COLUMN task_status.created_at IS 'Timestamp when the record was created';
COMMENT ON COLUMN task_status.updated_at IS 'Timestamp when the record was last updated';

-- CREATE TABLE task
CREATE TABLE task (
    id              SERIAL PRIMARY KEY,
    name            VARCHAR NOT NULL,
    type_id         INT NOT NULL,
    status_id       INT NOT NULL,
    config          JSONB NOT NULL DEFAULT '{}',
    changelog_id    INT NOT NULL DEFAULT -1,
    created_at      TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at      TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
COMMENT ON TABLE task IS 'Stores information about the tasks created and managed within the system';
COMMENT ON COLUMN task.id IS 'Unique identifier for each task, auto-incremented';
COMMENT ON COLUMN task.name IS 'Name of the task';
COMMENT ON COLUMN task.type_id IS 'Foreign key referencing the type of the task';
COMMENT ON COLUMN task.status_id IS 'Foreign key referencing the status of the task';
COMMENT ON COLUMN task.config IS 'Configuration details for the task stored as JSONB';
COMMENT ON COLUMN task.changelog_id IS 'Reference ID to track changes';
COMMENT ON COLUMN task.created_at IS 'Timestamp when the record was created';
COMMENT ON COLUMN task.updated_at IS 'Timestamp when the record was last updated';
