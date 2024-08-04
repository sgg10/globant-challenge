-- changeset sebastian.granda:1

-- comment: department foreign keys
ALTER TABLE department
    ADD CONSTRAINT fk_department_created_by_task_id
    FOREIGN KEY (created_by_task_id)
    REFERENCES task(id);

-- comment: job foreign keys
ALTER TABLE job
    ADD CONSTRAINT fk_job_created_by_task_id
    FOREIGN KEY (created_by_task_id)
    REFERENCES task(id);

-- comment: employee foreign keys
ALTER TABLE employee
    ADD CONSTRAINT fk_employee_department_id
    FOREIGN KEY (department_id)
    REFERENCES department(id);

ALTER TABLE employee
    ADD CONSTRAINT fk_employee_job_id
    FOREIGN KEY (job_id)
    REFERENCES job(id);

ALTER TABLE employee
    ADD CONSTRAINT fk_employee_created_by_task_id
    FOREIGN KEY (created_by_task_id)
    REFERENCES task(id);

-- comment: task foreign keys
ALTER TABLE task
    ADD CONSTRAINT fk_task_type_id
    FOREIGN KEY (type_id)
    REFERENCES task_type(id);

ALTER TABLE task
    ADD CONSTRAINT fk_task_status_id
    FOREIGN KEY (status_id)
    REFERENCES task_status(id);
