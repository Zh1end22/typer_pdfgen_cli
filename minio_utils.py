import boto3

def get_minio_client():
    return boto3.client(
        "s3",
        endpoint_url="http://127.0.0.1:9000",  # Your MinIO server
        aws_access_key_id="minioadmin",
        aws_secret_access_key="minioadmin",
    )
