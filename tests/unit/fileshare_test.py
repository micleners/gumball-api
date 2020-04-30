from unittest import mock
from opshub import fileshare
import hamcrest as ham


def test_create_client():
    app = mock.Mock()
    app.config = {
        'S3_ENDPOINT_URL': 'somewhere',
        'S3_ACCESS_KEY_ID': '12345',
        'S3_SECRET_ACCESS_KEY': 'abcdef'
    }

    with mock.patch('boto3.client') as boto3_create_client:
        client = fileshare.create_client(app)
        ham.assert_that(client, ham.is_(boto3_create_client.return_value))
        boto3_create_client.assert_called_once_with('s3',
                                                    aws_access_key_id='12345',
                                                    aws_secret_access_key='abcdef')
