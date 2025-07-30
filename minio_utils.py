import boto3

def get_minio_client():
    return boto3.client(
        "s3",
        endpoint_url="",  # put ur MinIO endpt api
        aws_access_key_id="minioadmin",
        aws_secret_access_key="minioadmin",
    )
