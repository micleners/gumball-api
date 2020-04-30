"""
S3 access
"""
import typing

import boto3

if typing.TYPE_CHECKING:
    import flask
    import boto3_type_annotations.s3 as boto_s3


def create_client(app: 'flask.Flask') -> 'boto_s3.Client':
    """
    Create an S3 client from configuration stored in a Flask app
    """
    return boto3.client('s3',
                        aws_access_key_id=app.config.get('S3_ACCESS_KEY_ID'),
                        aws_secret_access_key=app.config.get('S3_SECRET_ACCESS_KEY'))
