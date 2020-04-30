import os
import io
import tempfile

import pytest
from unittest import mock
from unittest.mock import patch
import opshub


@pytest.fixture(scope='module')
def test_client():
    app = opshub.create_app()
    app.config['TESTING'] = True
    app.config['S3_ENDPOINT_URL'] = 'S3_ENDPOINT_URL'
    app.config['S3_BUCKET_NAME'] = 'S3_BUCKET_NAME'
    app.config['S3_ACCESS_KEY_ID'] = 'S3_ACCESS_KEY_ID'
    app.config['S3_SECRET_ACCESS_KEY'] = 'S3_SECRET_ACCESS_KEY'
    testing_client = app.test_client()
    return testing_client  # this is where the testing happens!


def test_home(test_client, monkeypatch):
    response = test_client.get('/')
    assert response.status_code == 200
    assert response.data.decode('utf-8') == 'apples'


# @patch('opshub.fileshare')
@patch('opshub.s3_helpers')
# def test_upload_endpoint(fileshare, create_client, test_client):
def test_upload_endpoint(s3_helpers, test_client):
    filename = 'test1.txt'
    s3_helpers.upload_file.return_value = filename
    # fileshare.create_client.return_value = 'mock_fileshare'

    data = {'technician-id': '001', 'machine-id': 'M001'}
    data['file'] = (io.BytesIO(b"abcdef"), filename)
    response = test_client.post(
        '/upload', data=data,
        content_type='multipart/form-data'
    )

    # s3_helpers.upload_file.assert_called_with(
    #     'mock_fileshare', data['file'], '001', 'M001')

    assert response.status_code == 200
    assert response.data.decode('utf-8') == filename


# @pytest.fixture
# def client():
#     app = create_app()
#     app.testing = True
#     client = app.test_client()
#     # apples = app.upload()
#     # assert apples == 'apples'
#     return client


# def test_home(client):
#     print(client)
