from uuid import uuid4
from pathlib import Path
from datetime import datetime

import pandas as pd
from sqlalchemy import extract, func
from jinja2 import Environment, FileSystemLoader

from aws.s3 import create_presigned_url, upload
from database.models import Department, Employee, Job
import constants


template_loader = FileSystemLoader(searchpath=f"{Path(__file__).parent}/templates")
template_env = Environment(loader=template_loader)


def load_template(template_file: str):
    """
    Load a template file.

    Args:
        template_file (str): The path to the template file.

    Returns:
        template: The loaded template object.
    """
    template = template_env.get_template(template_file)
    return template


def get_employee_counts_by_quarter(session):
    """
    Retrieves the employee counts by quarter for each department and job.

    Args:
        session: The database session object.

    Returns:
        A pandas DataFrame containing the employee counts by quarter for each department and job.
        The DataFrame has the following columns: department, job, Q1, Q2, Q3, Q4.
    """
    results = (
        session.query(
            Department.department,
            Job.job,
            extract("quarter", Employee.datetime).label("quarter"),
            func.count(Employee.id).label("count"),
        )
        .join(Employee, Employee.department_id == Department.id)
        .join(Job, Employee.job_id == Job.id)
        .filter(func.date_part("year", Employee.datetime) == 2021)
        .group_by(Department.department, Job.job, "quarter")
        .order_by(Department.department, Job.job)
        .all()
    )

    data = []
    for department, job, quarter, count in results:
        data.append(
            {
                "department": department,
                "job": job,
                "quarter": int(quarter),
                "count": count,
            }
        )

    df = pd.DataFrame(data)
    if df.empty:
        return pd.DataFrame(columns=["department", "job", "Q1", "Q2", "Q3", "Q4"])

    df_pivot = df.pivot_table(
        index=["department", "job"], columns="quarter", values="count", fill_value=0
    ).reset_index()

    df_pivot.columns = ["department", "job"] + [
        f"Q{int(col)}" for col in df_pivot.columns[2:]
    ]

    df_sorted = df_pivot.sort_values(by=["department", "job"])

    return df_sorted


def get_departments_hiring_above_mean(session):
    """
    Retrieves the departments that have hired above the mean number of employees in the given session.

    Args:
        session: The session object used for querying the database.

    Returns:
        A sorted DataFrame containing the departments that have hired above the mean number of employees.
        The DataFrame has three columns: 'id' (department ID), 'department' (department name), and 'hired' (number of employees hired).

    Raises:
        None.
    """

    dept_hiring_counts = (
        session.query(
            Department.id, Department.department, func.count(Employee.id).label("hired")
        )
        .join(Employee, Employee.department_id == Department.id)
        .filter(func.date_part("year", Employee.datetime) == 2021)
        .group_by(Department.id, Department.department)
        .all()
    )

    df = pd.DataFrame(dept_hiring_counts, columns=["id", "department", "hired"])
    mean_hired = df["hired"].mean()

    df_filtered = df[df["hired"] > mean_hired]

    df_sorted = df_filtered.sort_values(by="hired", ascending=False)

    return df_sorted


def render_template_to_md(data, report_name, template):
    """
    Renders a template to Markdown format.

    Args:
        data (dict): The data to be passed to the template.
        report_name (str): The name of the report.
        template (Template): The template object to render.

    Returns:
        str: The rendered Markdown content.
    """
    creation_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    md_content = template.render(
        report_name=report_name, creation_date=creation_date, data=data
    )
    return md_content


CONFIG_MAP = {
    "type1": {
        "template": constants.REPORT_TYPE1_TEMPLATE,
        "name": constants.REPORT_TYPE1_NAME,
        "output": constants.REPORT_TYPE1_OUTPUT,
        "function": get_employee_counts_by_quarter,
    },
    "type2": {
        "template": constants.REPORT_TYPE2_TEMPLATE,
        "name": constants.REPORT_TYPE2_NAME,
        "output": constants.REPORT_TYPE2_OUTPUT,
        "function": get_departments_hiring_above_mean,
    },
}


def run(data, session, *args, **kwargs):
    """
    Run the report generation process.

    Args:
        data (dict): A dictionary containing the report type.
        session: The session object for database connection.
        *args: Variable length argument list.
        **kwargs: Arbitrary keyword arguments.

    Returns:
        tuple: A tuple containing the generated report and an error message, if any.

    Raises:
        Exception: If an error occurs during the report generation process.
    """
    try:
        report_config = CONFIG_MAP[data["report_type"]]

        df = report_config["function"](session)
        report_data = df.to_dict(orient="records")
        md_content = render_template_to_md(
            report_data,
            report_config["name"],
            load_template(report_config["template"]),
        )

        bucket_name = constants.S3_BUCKET_NAME
        object_name = f"reports/{report_config['output']}-{uuid4()}.md"
        if not upload(md_content, bucket_name, object_name):
            return None, constants.REPORT_FAIL_S3_UPLOAD

        presigned_url = create_presigned_url(bucket_name, object_name, 3600 * 60 * 24)
        if not presigned_url:
            return None, constants.REPORT_FAIL_URL_GENERATION

        return {
            "message": constants.REPORT_GENERATED_SUCCESS,
            "url": presigned_url,
        }, None
    except Exception as e:
        return None, str(e)
