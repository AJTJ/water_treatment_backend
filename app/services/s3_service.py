import boto3
import os
from botocore.exceptions import BotoCoreError, ClientError
from dotenv import load_dotenv
from mypy_boto3_s3 import S3Client
import uuid
from datetime import datetime

load_dotenv()

s3_client: S3Client = boto3.client(  # type: ignore
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION"),
)

BUCKET_NAME = os.getenv("S3_BUCKET_NAME", "")
CLOUDFRONT_URL = os.getenv("CLOUDFRONT_DISTRIBUTION_URL")


def upload_file_to_s3(file_content: bytes, filename: str) -> str:
    """
    Uploads a file to the specified S3 bucket and returns the CloudFront URL.

    :param file_content: Content of the file to be uploaded.
    :param filename: The name to save the file as in S3.
    :return: The CloudFront URL of the uploaded file.
    """
    try:
        # Generate a unique filename using UUID and timestamp
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        unique_filename = f"{timestamp}-{uuid.uuid4()}-{filename}"

        s3_client.put_object(Bucket=BUCKET_NAME, Key=unique_filename, Body=file_content)
        return f"{CLOUDFRONT_URL}/{unique_filename}"
    except (BotoCoreError, ClientError) as e:
        raise Exception(f"Error uploading file to S3: {str(e)}")
