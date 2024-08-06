import logging

import boto3
from botocore.exceptions import ClientError


def upload(data, bucket, object_name):
    """
    Uploads data to an S3 bucket.

    Args:
        data: The data to be uploaded.
        bucket: The name of the S3 bucket.
        object_name: The name of the object in the S3 bucket.

    Returns:
        bool: True if the upload is successful, False otherwise.
    """
    s3_client = boto3.client("s3")
    try:
        response = s3_client.put_object(Bucket=bucket, Key=object_name, Body=data)
    except ClientError as e:
        logging.error(e)
        return False
    return True


def create_presigned_url(bucket_name, object_name, expiration=3600):
    """
    Generates a presigned URL for accessing an object in an S3 bucket.

    Parameters:
        bucket_name (str): The name of the S3 bucket.
        object_name (str): The key of the object in the S3 bucket.
        expiration (int, optional): The expiration time of the presigned URL in seconds. Defaults to 3600.

    Returns:
        str: The presigned URL for accessing the object.

    Raises:
        ClientError: If there is an error generating the presigned URL.
    """

    s3_client = boto3.client("s3")
    try:
        response = s3_client.generate_presigned_url(
            "get_object",
            Params={"Bucket": bucket_name, "Key": object_name},
            ExpiresIn=expiration,
        )
    except ClientError as e:
        logging.error(e)
        return None

    return response


def download(bucket_name, object_name):
    """
    Downloads an object from an S3 bucket.

    Args:
        bucket_name (str): The name of the S3 bucket.
        object_name (str): The name of the object to download.

    Returns:
        bytes: The content of the downloaded object.

    Raises:
        ClientError: If there is an error while downloading the object.
    """
    s3_client = boto3.client("s3")
    try:
        response = s3_client.get_object(Bucket=bucket_name, Key=object_name)
    except ClientError as e:
        logging.error(e)
        return None
    return response["Body"].read()
