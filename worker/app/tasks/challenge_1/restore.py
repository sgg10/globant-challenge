import pandas as pd
from io import BytesIO

import constants
from aws.s3 import download


def parquet_to_df(parquet_data):
    """
    Converts parquet data to a pandas DataFrame.

    Args:
        parquet_data (bytes): The parquet data to be converted.

    Returns:
        pandas.DataFrame: The converted DataFrame.
    """
    return pd.read_parquet(BytesIO(parquet_data))


def insert_data_to_db(df, table_name, session):
    """
    Insert data from a DataFrame into a database table.

    Args:
        df (pandas.DataFrame): The DataFrame containing the data to be inserted.
        table_name (str): The name of the database table to insert the data into.
        session: The database session object.

    Returns:
        None
    """
    model = constants.BASE_CHALLENGE_1_CONFIG_MAP[table_name]["model"]
    session.bulk_insert_mappings(model, df.to_dict(orient="records"))
    session.commit()


def run(data, session, *args, **kwargs):
    """
    Restores a table from a Parquet file stored in an S3 bucket.

    Args:
        data (dict): A dictionary containing the table_name key specifying the name of the table to restore.
        session: The session object for the database connection.
        *args: Variable length argument list.
        **kwargs: Arbitrary keyword arguments.

    Returns:
        tuple: A tuple containing the restore result and an error message (if any). The restore result is a dictionary
        with a "message" key indicating the status of the restore operation. The error message is None if the restore
        operation is successful, otherwise it contains a string describing the error.

    Raises:
        Exception: If an error occurs during the restore operation.
    """

    try:
        table_name = data["table_name"]
        bucket_name = constants.S3_BUCKET_NAME
        parquet_data = download(
            bucket_name, f"{constants.S3_BACKUP_PATH}/{table_name}.parquet"
        )
        if parquet_data is None:
            return None, constants.RESTORE_NOT_FOUND_IN_S3

        df = parquet_to_df(parquet_data)
        insert_data_to_db(df, table_name, session)
        return {"message": constants.RESTORE_SUCCESS(table_name)}, None
    except Exception as e:
        return None, str(e)
