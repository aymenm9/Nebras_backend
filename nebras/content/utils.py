import boto3
from django.conf import settings
from uuid import uuid4
from .models import R2File
from typing import Literal

def get_s3_client():
    '''
    Returns a boto3 client for S3
    '''
    return boto3.client(
        's3',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_REGION
    )

def generate_presigned_url(file: R2File,method: Literal['get', 'put'] = 'get'):
    '''
        Generate a presigned url for S3
        params:
            file : R2File
            method : get or put
        return:
            presigned url
    '''
    s3 = get_s3_client()
    
    upload_url = s3.generate_presigned_url(
        f'{method}_object',
        Params={
            'Bucket': settings.AWS_STORAGE_BUCKET_NAME,
            'Key': file.file_key,
            'ContentType': file.file_type,
        },
        ExpiresIn=3600
    )
    return upload_url



def create_file_key(section: str,subsection: str, secondary_subsection: str = None, file_type: Literal['video', 'audio', 'document'] = 'video'):
    directory = f'{section}/{subsection}/'
    directory += f'{secondary_subsection}/' if secondary_subsection else ''
    directory += f'{file_type}/'
    return directory + str(uuid4())