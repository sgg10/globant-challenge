from sqlalchemy import (
    JSON,
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    func,
)
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Department(Base):
    """
    Represents a department in the organization.

    Attributes:
        id (int): The unique identifier of the department.
        department (str): The name of the department.
        changelog_id (int): The identifier of the changelog associated with the department.
        created_by_task_id (int): The identifier of the task that created the department.
        created_at (datetime): The timestamp when the department was created.
        updated_at (datetime): The timestamp when the department was last updated.
    """

    __tablename__ = "department"
    id = Column(Integer, primary_key=True, autoincrement=True)
    department = Column(String, nullable=False)
    changelog_id = Column(Integer, default=-1, nullable=False)
    created_by_task_id = Column(Integer, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime, onupdate=func.now(), default=func.now(), nullable=False
    )


class Job(Base):
    """
    Represents a job entity.

    Attributes:
        id (int): The unique identifier of the job.
        job (str): The name of the job.
        changelog_id (int): The ID of the associated changelog.
        created_by_task_id (int): The ID of the task that created the job.
        created_at (datetime): The timestamp when the job was created.
        updated_at (datetime): The timestamp when the job was last updated.
    """

    __tablename__ = "job"
    id = Column(Integer, primary_key=True, autoincrement=True)
    job = Column(String, nullable=False)
    changelog_id = Column(Integer, default=-1, nullable=False)
    created_by_task_id = Column(Integer, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime, onupdate=func.now(), default=func.now(), nullable=False
    )


class Employee(Base):
    """
    Represents an employee in the company.

    Attributes:
        id (int): The unique identifier of the employee.
        name (str): The name of the employee.
        datetime (datetime): The date and time when the employee record was created.
        department_id (int): The ID of the department the employee belongs to.
        job_id (int): The ID of the job position the employee holds.
        changelog_id (int): The ID of the changelog associated with the employee.
        created_by_task_id (int): The ID of the task that created the employee record.
        created_at (datetime): The date and time when the employee record was created.
        updated_at (datetime): The date and time when the employee record was last updated.
    """

    __tablename__ = "employee"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    datetime = Column(DateTime, nullable=False)
    department_id = Column(Integer, ForeignKey("department.id"), nullable=False)
    job_id = Column(Integer, ForeignKey("job.id"), nullable=False)
    changelog_id = Column(Integer, default=-1, nullable=False)
    created_by_task_id = Column(Integer, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime, onupdate=func.now(), default=func.now(), nullable=False
    )


class TaskType(Base):
    """
    Represents a task type.

    Attributes:
        id (int): The primary key of the task type.
        name (str): The name of the task type.
        changelog_id (int): The changelog ID of the task type.
        created_at (datetime): The creation date and time of the task type.
        updated_at (datetime): The last update date and time of the task type.
    """

    __tablename__ = "task_type"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    changelog_id = Column(Integer, default=-1, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime, onupdate=func.now(), default=func.now(), nullable=False
    )


class TaskStatus(Base):
    """
    TaskStatus Model

    This class represents the TaskStatus model in the migration pipeline.

    Attributes:
        id (int): The primary key of the TaskStatus.
        name (str): The name of the TaskStatus.
        changelog_id (int): The changelog ID of the TaskStatus.
        created_at (datetime): The creation timestamp of the TaskStatus.
        updated_at (datetime): The last update timestamp of the TaskStatus.
    """

    __tablename__ = "task_status"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    changelog_id = Column(Integer, default=-1, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime, onupdate=func.now(), default=func.now(), nullable=False
    )


class Task(Base):
    """
    Represents a task in the migration pipeline.

    Attributes:
        id (int): The unique identifier of the task.
        name (str): The name of the task.
        type_id (int): The ID of the task type.
        status_id (int): The ID of the task status.
        config (dict): The configuration of the task.
        start_at (datetime): The start time of the task.
        end_at (datetime): The end time of the task.
        changelog_id (int): The ID of the task's changelog.
        created_at (datetime): The creation time of the task.
        updated_at (datetime): The last update time of the task.
    """

    __tablename__ = "task"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    type_id = Column(Integer, ForeignKey("task_type.id"), nullable=False)
    status_id = Column(Integer, ForeignKey("task_status.id"), nullable=False)
    config = Column(JSON, default="{}", nullable=False)
    start_at = Column(DateTime, nullable=False)
    end_at = Column(DateTime)
    changelog_id = Column(Integer, default=-1, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime, onupdate=func.now(), default=func.now(), nullable=False
    )
