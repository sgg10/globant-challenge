import logging
import pandas as pd
from sqlalchemy.exc import IntegrityError

import constants
from database.models import Department, Employee, Job


def validate_data(df):
    """
    Validates the given DataFrame by removing rows that contain any null values.

    Args:
        - df: pandas.DataFrame
            The DataFrame to be validated.

    Returns:
        - valid_rows: pandas.DataFrame
            The DataFrame with valid rows (rows without any null values).
        - invalid_rows: pandas.DataFrame
            The DataFrame with invalid rows (rows containing null values).
    """
    invalid_rows = df[df.isnull().any(axis=1)]
    valid_rows = df.drop(invalid_rows.index)
    return valid_rows, invalid_rows


def load_data(data, model, session, task_id, *args, **kwargs):
    """
    Load data into a database table.

    Args:
        data (list): The data to be loaded into the table.
        model (SQLAlchemy model): The SQLAlchemy model representing the table.
        session (SQLAlchemy session): The SQLAlchemy session object.
        task_id (int): The ID of the task associated with the data.
        *args: Additional positional arguments.
        **kwargs: Additional keyword arguments.

    Returns:
        tuple: A tuple containing a boolean indicating whether the data was loaded successfully and any error message if applicable.
    """
    model_name = model.__tablename__

    try:
        df = pd.DataFrame(data)

        valid_data, invalid_data = validate_data(df)

        valid_data.loc[:, ("created_by_task_id",)] = task_id

        try:
            valid_data.to_sql(
                model_name, session.get_bind(), if_exists="append", index=False
            )
        except IntegrityError as e:
            if not constants.LOAD_DUPLICATE_KEY_VALUE_ERROR in str(e):
                raise e
            logging.warning(f"{constants.LOAD_CANNOT_INSERT_DUPLICATE}: {e}")

        session.commit()

        if not invalid_data.empty:
            for _, row in invalid_data.iterrows():
                logging.warning(constants.LOAD_INVALID_ROW(row.to_dict()))
            return True, constants.LOAD_INVALID_ROWS_FOUND(model_name)

        return True, None
    except Exception as e:
        return False, e


def run(data, session, task_id, *args, **kwargs):
    """
    Loads data into the specified models based on the configuration map.

    Args:
        data (dict): A dictionary containing the data to be loaded. The keys should correspond to the keys in the configuration map.
        session: The session object for the database connection.
        task_id: The ID of the task.
        *args: Additional positional arguments.
        **kwargs: Additional keyword arguments.

    Returns:
        tuple: A tuple containing the result and any error message. The result is a dictionary with a "message" key indicating the success of the data loading operation, and a "warning" key containing any warning message. The error message is None if the data loading was successful.

    """
    for key, config in constants.LOAD_CHALLENGE_1_CONFIG_MAP.items():
        model = config["model"]
        _data = data.get(key, [])

        if not _data:
            continue

        success, error = load_data(_data, model, session, task_id)

        if not success:
            return None, error

    return {"message": constants.LOAD_DATA_SUCCESS, "warning": error}, None
