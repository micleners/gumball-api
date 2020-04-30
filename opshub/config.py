import os
import logging
from opshub import util

logger = logging.getLogger(__name__)

S3_ENDPOINT_URL = os.getenv('S3_ENDPOINT_URL', 'http://localhost:9000')
S3_BUCKET_NAME =  os.getenv('S3_BUCKET_NAME', 'gumball-data')
S3_ACCESS_KEY_ID =  os.getenv('S3_ACCESS_KEY_ID', 'AKIAIOSFODNN7EXAMPLE')
S3_SECRET_ACCESS_KEY =  os.getenv('S3_SECRET_ACCESS_KEY', 'wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY')

SQLALCHEMY_DB_URL = f'postgresql://postgres:secret@localhost:{os.getenv("DB_PORT", "5432")}/postgres'

# !!!!Keep config values above this line!!!!

logger.debug('Updating config from environment')
util.update_from_env(globals())
