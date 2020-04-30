import io
import tempfile
from unittest.mock import MagicMock, Mock

import boto3
from botocore.stub import Stubber

from opshub import s3_helpers


def test_upload_file():
    client = boto3.client('s3')
    stubber = Stubber(client)
    stubber.activate()

    s3 = MagicMock()
    bucket_name = 'data_bucket'
    filename = 'somefile.txt'
    file = Mock()
    file.filename = filename
    tech_id = '0202'
    mach_id = '0101'

    response = s3_helpers.upload_file(s3, bucket_name, file, tech_id, mach_id)

    assert response == 'somefile'
