import io
import os
import unittest
from unittest.mock import MagicMock, Mock
from datetime import datetime
import tempfile

import pytest
import botocore
from botocore.stub import Stubber
import boto3

from opshub import s3_helpers


class UploadFile(unittest.TestCase):

    def setUp(self):
        self.s3 = MagicMock()
        self.bucket_name = 'data_bucket'
        self.now = datetime.fromisoformat('2020-05-01 15:37:23.143534-05:00')
        self.tech_id = '0202'
        self.mach_id = '0101'
        self.file = mock_file('somefile.txt')
        self.file.save = Mock()

    def test_returns_name_of_file(self):
        expected_file_name = f'T{self.tech_id}/T{self.tech_id}.{self.mach_id}.{self.now}.txt'

        self.response = s3_helpers.upload_file(
            self.s3, self.bucket_name, self.file, self.tech_id, self.mach_id, self.now)

        assert self.response == expected_file_name

    def test_calls_s3_with_correct_parameters(self):
        s3_helpers.UPLOAD_PATH = '/dir/path'
        expected_file_path = os.path.join('/dir/path', self.file.filename)
        expected_file_name = f'T{self.tech_id}/T{self.tech_id}.{self.mach_id}.{self.now}.txt'

        s3_helpers.upload_file(self.s3, self.bucket_name,
                               self.file, self.tech_id, self.mach_id, self.now)

        self.s3.upload_file.assert_called_with(
            expected_file_path, self.bucket_name, expected_file_name)

    def test_returns_error_message_when_s3_blows_up(self):
        operation_name = 'UploadPartCopy'
        parsed_response = {
            'Error': {'Code': '500', 'Message': 'Error Uploading'}}
        clientError = botocore.exceptions.ClientError(
            parsed_response, operation_name)
        self.s3.upload_file = Mock(side_effect=clientError)

        response = s3_helpers.upload_file(
            self.s3, self.bucket_name, self.file, self.tech_id, self.mach_id, self.now)

        assert response == "An error occurred (500) when calling the UploadPartCopy operation: Error Uploading"


class GetFileNames(unittest.TestCase):

    def setUp(self):
        self.bucket_name = 'data_bucket'
        self.tech_id = '0202'

        self.s3 = boto3.client('s3')
        stubber = Stubber(self.s3)
        self.mock_response = mock_response()
        stubber.add_response('list_objects', self.mock_response)
        stubber.activate()

    def test_returns_the_correct_number_of_objects(self):
        response = s3_helpers.get_file_names(
            self.s3, self.bucket_name, self.tech_id)
        assert len(response) == 3

    def test_returns_the_correct_list_of_files(self):
        response = s3_helpers.get_file_names(
            self.s3, self.bucket_name, self.tech_id)
        assert response == ['T0202.GM0202.2020-04-28_205630.txt',
                            'T0202.GM0202.2020-04-28_205829.txt', 'T0303.GM0303.2020-04-28_205831.txt']

    def test_returns_error_message_when_s3_blows_up(self):
        self.s3 = MagicMock()
        operation_name = 'DownloadFiles'
        parsed_response = {
            'Error': {'Code': '500', 'Message': 'Error Fetching'}}
        clientError = botocore.exceptions.ClientError(
            parsed_response, operation_name)
        self.s3.list_objects = Mock(side_effect=clientError)

        response = s3_helpers.get_file_names(
            self.s3, self.bucket_name, self.tech_id)

        assert response == "An error occurred (500) when calling the DownloadFiles operation: Error Fetching"



def mock_file(filename):
    file = Mock()
    file.filename = filename
    return file


def mock_response():
    return {
        'Contents':
        [
            {
                'ETag': '"d41d8cd98f00b204e9800998ecf8427e"',
                'Key': 'T0202/T0202.GM0202.2020-04-28_205630.txt',
                'Owner': {'ID': '8db562505766921cfbc1bd612f0300b03b0a43524579b54af4a6825b8610a57a'},
                'Size': 0,
                'StorageClass': 'STANDARD'
            },
            {
                'ETag': '"d41d8cd98f00b204e9800998ecf8427e"',
                'Key': 'T0202/T0202.GM0202.2020-04-28_205829.txt',
                'Owner': {'ID': '8db562505766921cfbc1bd612f0300b03b0a43524579b54af4a6825b8610a57a'},
                'Size': 0,
                'StorageClass': 'STANDARD'
            },
            {
                'ETag': '"d41d8cd98f00b204e9800998ecf8427e"',
                'Key': 'T0202/T0303.GM0303.2020-04-28_205831.txt',
                'Owner': {'ID': '8db562505766921cfbc1bd612f0300b03b0a43524579b54af4a6825b8610a57a'},
                'Size': 0,
                'StorageClass': 'STANDARD'
            },
            {
                'ETag': '"d41d8cd98f00b204e9800998ecf8427e"',
                'Key': 'T001/T001.GM001.2020-04-28_205834.txt',
                'Owner': {'ID': '8db562505766921cfbc1bd612f0300b03b0a43524579b54af4a6825b8610a57a'},
                'Size': 0,
                'StorageClass': 'STANDARD'
            }
        ]
    }
