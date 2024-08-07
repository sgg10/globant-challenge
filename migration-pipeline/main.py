import logging
from datetime import datetime

import pandas as pd
from sqlalchemy.exc import IntegrityError


from constants import TABLES
from models import Task, TaskType, TaskStatus, Session

logging.basicConfig(
    level=logging.INFO, format="[%(levelname)s | %(asctime)s] %(message)s"
)


def get_id_by_name(session, model, name):
    """
    Fetch the ID of a record from a model based on its name.
    """
    record = session.query(model).filter_by(name=name).first()
    return record.id if record else None


def validate_data(df):
    """
    Validate the dataframe by checking if all columns have non-null values.
    """
    invalid_rows = df[df.isnull().any(axis=1)]
    valid_rows = df.dropna()
    return valid_rows, invalid_rows


def migrate_data(file_path, model, session, task_id, columns):
    """
    Migrate data from a CSV file to the database using the specified model.
    """
    model_name = model.__tablename__

    print(f"Migrating {model_name}")

    df = pd.read_csv(
        file_path,
        header=None,
        names=columns,
    )

    valid_data, invalid_data = validate_data(df)

    # Log invalid rows
    if not invalid_data.empty:
        for _, row in invalid_data.iterrows():
            logging.warning(f"Invalid row {row.to_dict()}: missing required fields")

    valid_data.loc[:, ("created_by_task_id",)] = task_id

    try:
        valid_data.to_sql(
            model_name, session.get_bind(), if_exists="append", index=False
        )
    except IntegrityError as e:
        if not "duplicate key value violates unique constraint" in str(e):
            raise e
        logging.warning(f"Cannot insert duplicate data into {model_name}")

    session.commit()

    print(f"\t{len(valid_data)} rows migrated")


def main():
    session = Session()

    # Obtaining IDs for task type and status
    migration_type_id = get_id_by_name(session, TaskType, "MIGRATION")
    in_progress_status_id = get_id_by_name(session, TaskStatus, "IN_PROGRESS")
    completed_status_id = get_id_by_name(session, TaskStatus, "COMPLETED")
    failed_status_id = get_id_by_name(session, TaskStatus, "FAILED")

    # Create a new task for migration
    migration_task = Task(
        name="Migration",
        type_id=migration_type_id,
        status_id=in_progress_status_id,
        start_at=datetime.now(),
    )
    session.add(migration_task)
    session.commit()

    task_id = migration_task.id

    try:
        for table in TABLES:
            migrate_data(
                table["filename"],
                table["model"],
                session,
                task_id,
                table["columns"],
            )

        # Update the migration task status to completed
        migration_task.status_id = completed_status_id
        migration_task.updated_at = datetime.now()
        migration_task.end_at = datetime.now()
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"Error migrating data: {e}")
        logging.error(f"Error committing transaction: {e}")
        migration_task.status_id = failed_status_id
        migration_task.updated_at = datetime.now()
        migration_task.end_at = datetime.now()
        session.commit()
    finally:
        session.close()


if __name__ == "__main__":
    main()
