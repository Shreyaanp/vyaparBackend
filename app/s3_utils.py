import boto3
from botocore.exceptions import NoCredentialsError
from dotenv import load_dotenv
import os

load_dotenv()

s3 = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
)

def upload_file_to_s3(file, bucket_name, object_name):
    try:
        s3.upload_fileobj(file, bucket_name, object_name)
        return f"https://{bucket_name}.s3.amazonaws.com/{object_name}"
    except NoCredentialsError:
        return None

def upload_files_to_s3(files, bucket_name, object_prefix):
    links = []
    try:
        for file in files:
            object_name = f"{object_prefix}{file.filename}"
            s3.upload_fileobj(file.file, bucket_name, object_name)
            links.append(f"https://{bucket_name}.s3.amazonaws.com/{object_name}")
        return links
    except NoCredentialsError:
        return None
