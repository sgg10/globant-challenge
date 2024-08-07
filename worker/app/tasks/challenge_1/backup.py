import pandas as pd
from io import BytesIO

from aws.s3 import upload

import constants


def df_to_parquet(df):
    """
    Converts a pandas DataFrame to a Parquet file format.

    Args:
        df (pandas.DataFrame): The DataFrame to be converted.

    Returns:
        bytes: The Parquet file content as bytes.
    """
    output = BytesIO()
    df.to_parquet(output, index=False)
    return output.getvalue()


def get_all_data(table_name, session):
    """
    Retrieve all data from the specified table.

    Args:
        table_name (str): The name of the table.
        session: The database session.

    Returns:
        list: A list of all data retrieved from the table.
    """
    model = constants.BASE_CHALLENGE_1_CONFIG_MAP[table_name]["model"]
    return session.query(model).all()


def send_data_to_s3(data, table_name, bucket_name):
    """
    Sends the given data to an S3 bucket.

    Args:
        data: The data to be sent.
        table_name: The name of the table associated with the data.
        bucket_name: The name of the S3 bucket.

    Returns:
        The result of the upload operation.

    """
    return upload(data, bucket_name, f"{constants.S3_BACKUP_PATH}/{table_name}.parquet")


def run(data, session, *args, **kwargs):
    """
    Run the backup process for the specified table.
    """
    try:
        table_name = data["table_name"]
        bucket_name = constants.S3_BUCKET_NAME
        data = get_all_data(table_name, session)
        data = [
            {k: v for k, v in row.__dict__.items() if not k.startswith("_")}
            for row in data
        ]
        df = pd.DataFrame(data)
        parquet_data = df_to_parquet(df)
        result = send_data_to_s3(parquet_data, table_name, bucket_name)
        if not result:
            return None, constants.BACKUP_FAILED(table_name)
        return {"message": constants.BACKUP_SUCCESS(table_name)}, None
    except Exception as e:
        return None, e
