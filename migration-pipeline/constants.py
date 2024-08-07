import os

DB_NAME = os.getenv("POSTGRES_NAME", "mydb")
DB_USER = os.getenv("POSTGRES_USER", "postgres")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
DB_HOST = os.getenv("POSTGRES_HOST", "localhost")

import models

TABLES = (
    {
        "filename": "./data/departments.csv",
        "columns": ("id", "department"),
        "model": models.Department,
    },
    {"filename": "./data/jobs.csv", "columns": ("id", "job"), "model": models.Job},
    {
        "filename": "./data/hired_employees.csv",
        "columns": ("id", "name", "datetime", "department_id", "job_id"),
        "model": models.Employee,
    },
)
