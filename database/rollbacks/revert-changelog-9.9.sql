--liquibase formatted sql

--changeset rollback:0
--comment: Delete all records created by app (with changelog_id = -1)

DELETE FROM department WHERE changelog_id = -1;
DELETE FROM job WHERE changelog_id = -1;
DELETE FROM employee WHERE changelog_id = -1;
DELETE FROM task WHERE changelog_id = -1;
DELETE FROM task_status WHERE changelog_id = -1;
DELETE FROM task_type WHERE changelog_id = -1;
