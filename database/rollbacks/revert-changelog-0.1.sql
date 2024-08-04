--liquibase formatted sql

--changeset rollback:0
--comment: Delete the records created in the initial changelog, but keep the tables

DELETE FROM department WHERE changelog_id = 1;
DELETE FROM job WHERE changelog_id = 1;
DELETE FROM employee WHERE changelog_id = 1;
DELETE FROM task WHERE changelog_id = 1;
DELETE FROM task_status WHERE changelog_id = 1;
DELETE FROM task_type WHERE changelog_id = 1;
