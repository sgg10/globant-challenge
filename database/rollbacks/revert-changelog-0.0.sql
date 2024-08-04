--liquibase formatted sql

--changeset rollback:0
--comment: Drop the tables created in the initial changelog

DROP TABLE IF EXISTS employee CASCADE;
DROP TABLE IF EXISTS job CASCADE;
DROP TABLE IF EXISTS department CASCADE;
DROP TABLE IF EXISTS task CASCADE;
DROP TABLE IF EXISTS task_status CASCADE;
DROP TABLE IF EXISTS task_type CASCADE;
