import boto3
from django.conf import settings
from uuid import uuid4
from .models import R2File
from typing import Literal
from botocore.config import Config
from .models import Metadata, Part, MultipartUpload

def get_s3_client():
    '''
    Returns a boto3 client for S3
    '''
    return boto3.client(
        's3',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_REGION,
        endpoint_url=settings.AWS_S3_ENDPOINT_URL,
        config=Config(signature_version='s3v4')
    )

def generate_presigned_url(file: R2File,method: Literal['get_object', 'put_object'] = 'get_object'):
    '''
        Generate a presigned url for S3
        params:
            file : R2File
            method : get_object or put_object
        return:
            presigned url
    '''
    s3 = get_s3_client()
    
    params = {
        'Bucket': settings.AWS_STORAGE_BUCKET_NAME,
        'Key': file.file_key,
    }
    if method == 'put_object':
        params['ContentType'] = file.file_type
        params['ContentLength'] = file.file_size
        params['Metadata'] = {'user-id': str(file.metadata.created_by.id), 'file-id': str(file.id), 'upload-type': file.upload_type}
    
    upload_url = s3.generate_presigned_url(
        ClientMethod=method,
        Params=params,
        ExpiresIn=3600
    )
    return upload_url

def generate_presigned_url_for_part(file: R2File, part_number: int , UploadId: str = None):
    '''
        Generate a presigned url for S3
        params:
            file : R2File
            method : get_object or put_object or upload_part
        return:
            presigned url
    '''
    s3 = get_s3_client()
    
    params = {
        'Bucket': settings.AWS_STORAGE_BUCKET_NAME,
        'Key': file.file_key,
        'PartNumber': part_number,
        'UploadId': UploadId if UploadId else file.multipart_uploader.upload_id, # in case i need it for something else
        'ContentLength' : settings.PART_SIZE
    }

    upload_url = s3.generate_presigned_url(
        ClientMethod='upload_part',
        Params=params,
        ExpiresIn=3600
    )
    return upload_url



def create_file_key(section: str,subsection: str, secondary_subsection: str = None, file_type: Literal['video', 'audio', 'document'] = 'video'):
    directory = f'{section}/{subsection}/'
    directory += f'{secondary_subsection}/' if secondary_subsection else ''
    directory += f'{file_type}/'
    return directory + str(uuid4())
 
def create_multipart_upload(file: R2File):
    s3 = get_s3_client()
    response = s3.create_multipart_upload(
        Bucket=settings.AWS_STORAGE_BUCKET_NAME,
        Key=file.file_key,
        ContentType=file.file_type
    )

    return response['UploadId']


def get_parts_list(multipart_upload: MultipartUpload):
    return [{"PartNumber": p.part_number, "ETag": p.etag} for p in Part.objects.filter(multipart_upload=multipart_upload).order_by('part_number')]



def complete_multipart_upload(multipart_upload: MultipartUpload):
    s3 = get_s3_client()
    s3.complete_multipart_upload(
        Bucket=settings.AWS_STORAGE_BUCKET_NAME,
        Key=multipart_upload.r2_file.file_key,
        MultipartUpload={"Parts": get_parts_list(multipart_upload)},
        UploadId=multipart_upload.upload_id
    )

def clc_total_parts(file_size: int):
    return file_size // settings.PART_SIZE + 1


def get_next_part_number(multipart_upload: MultipartUpload):
    return Part.objects.filter(multipart_upload=multipart_upload, completed=True).count() + 1



def complete_r2_file(r2_file: R2File):
    if r2_file.upload_type == 'multipart':
        # check if all parts are completed
        if Part.objects.filter(multipart_upload=r2_file.multipart_uploader, completed=True).count() != r2_file.multipart_uploader.total_parts:
            return False
        complete_multipart_upload(r2_file.multipart_uploader)
        r2_file.multipart_uploader.completed = True
        r2_file.multipart_uploader.save()
    r2_file.upload_status = 'completed'
    r2_file.save()
    return True
        