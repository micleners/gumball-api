import os
from datetime import datetime

import botocore
from opshub.fileshare import create_client

UPLOAD_FOLDER = "uploads"
PROJECT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UPLOAD_PATH = os.path.join(PROJECT_PATH, UPLOAD_FOLDER)


def upload_file(s3, bucket_name, file, tech_id, mach_id):
    file_path = os.path.join(UPLOAD_PATH, file.filename)
    file.save(file_path)
    now = datetime.now().strftime('%Y-%m-%d_%H%M%S')

    try:
        file_name = f'T{tech_id}/T{tech_id}.{mach_id}.{now}.txt'
        s3.upload_file(file_path, bucket_name, file_name)
    except botocore.exceptions.ClientError as e:
        return str(e)

    return file_name


def get_file_names(s3, bucket_name, tech_id):
    bucket_objects = s3.list_objects(Bucket=bucket_name)['Contents']

    file_list_for_tech = [content['Key'] for content in bucket_objects if match_first_directory(
        content['Key'], tech_id)]

    file_list_trimmed = [second_argument(content)
                         for content in file_list_for_tech]

    return file_list_trimmed


def second_argument(content):
    split_content = content.split('/')
    return split_content[1]


def match_first_directory(content, tech_id):
    split_content = content.split('/')
    if len(split_content) != 2:
        return False
    else:
        return split_content[0] == f'T{tech_id}'
