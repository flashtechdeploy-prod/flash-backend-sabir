"""
File upload helper module.

Uploads files to Backblaze B2 cloud storage.
"""

import os
import uuid
from datetime import datetime
from typing import Tuple
from io import BytesIO

import boto3
from botocore.exceptions import ClientError
from fastapi import HTTPException
from app.core.config import settings


# Initialize Backblaze B2 S3-compatible client
def _get_b2_client():
    """Get Backblaze B2 S3-compatible client."""
    # Validate B2 credentials
    if not settings.B2_KEY_ID or not settings.B2_APPLICATION_KEY or not settings.B2_BUCKET_NAME:
        raise HTTPException(
            status_code=500,
            detail="B2 credentials not configured. Please set B2_KEY_ID, B2_APPLICATION_KEY, and B2_BUCKET_NAME environment variables."
        )
    
    return boto3.client(
        "s3",
        endpoint_url=settings.B2_ENDPOINT_URL,
        aws_access_key_id=settings.B2_KEY_ID,
        aws_secret_access_key=settings.B2_APPLICATION_KEY,
        region_name="us-east-005",
    )


async def upload_file_with_prefix(
    content: bytes,
    original_filename: str,
    prefix: str,
    content_type: str = "application/octet-stream",
    subdir: str = "uploads",
) -> Tuple[str, str]:
    """
    Upload a file to Backblaze B2 cloud storage.

    Returns:
        Tuple (file_url, new_filename)
    """

    ext = os.path.splitext(original_filename)[1] if original_filename else ""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    unique_id = str(uuid.uuid4())[:8]
    new_filename = f"{prefix}_{timestamp}_{unique_id}{ext}"

    # B2 object key (path in bucket)
    object_key = f"{subdir}/{new_filename}"

    try:
        b2_client = _get_b2_client()
        
        # Upload to Backblaze B2
        b2_client.upload_fileobj(
            BytesIO(content),
            settings.B2_BUCKET_NAME,
            object_key,
            ExtraArgs={"ContentType": content_type}
        )

        # Return public URL for the file
        file_url = f"{settings.B2_ENDPOINT_URL}/{settings.B2_BUCKET_NAME}/{object_key}"
        return file_url, new_filename

    except ClientError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Backblaze B2 upload failed: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Upload failed: {str(e)}"
        )


async def delete_file_from_b2(file_url: str) -> bool:
    """
    Delete a file from Backblaze B2.
    
    Args:
        file_url: The full URL of the file to delete
        
    Returns:
        True if deleted successfully, False otherwise
    """
    try:
        # Extract object key from URL
        # URL format: https://s3.us-west-004.backblazeb2.com/bucket-name/path/to/file
        bucket_prefix = f"{settings.B2_ENDPOINT_URL}/{settings.B2_BUCKET_NAME}/"
        if file_url.startswith(bucket_prefix):
            object_key = file_url[len(bucket_prefix):]
        else:
            # Try to extract from relative path
            object_key = file_url.lstrip("/")
        
        b2_client = _get_b2_client()
        b2_client.delete_object(
            Bucket=settings.B2_BUCKET_NAME,
            Key=object_key
        )
        return True
    except Exception:
        return False


def get_file_url(object_key: str) -> str:
    """
    Get the public URL for a file in B2.
    
    Args:
        object_key: The key/path of the file in the bucket
        
    Returns:
        Full public URL to the file
    """
    return f"{settings.B2_ENDPOINT_URL}/{settings.B2_BUCKET_NAME}/{object_key}"

