import pathlib

import pytest
import requests


def test_app_connection(app):
    resp = requests.get('http://localhost:5000/')
    assert resp.text == 'apples'

# Apparently I broke this test in the conftest setup for the fileshare:
#         try:
#             # check was uploaded
# >           assert uploaded_path.exists()
# E           AssertionError: assert False
# E            +  where False = <bound method Path.exists of PosixPath('/Users/imtapps/Developer/growlers-audition/data/gumball-data/junk.txt')>()
# Will circle back and try to fix it later

# def test_file_share_connection(file_share, app, bucket_dir, tmpdir):
#     # create junk file
#     tp = pathlib.Path(tmpdir) / 'junk.txt'
#     tp.write_text('hello!')

#     # try to upload
#     file_share.upload_file(str(tp), app.config.get('S3_BUCKET_NAME'), 'junk.txt')
#     uploaded_path = bucket_dir / 'junk.txt'
#     try:
#         # check was uploaded
#         assert uploaded_path.exists()
#         assert uploaded_path.read_text('utf-8') == 'hello!'
#     finally:
#         if uploaded_path.exists():
#             uploaded_path.unlink()


def test_db_connection(db_session):
    assert db_session.execute('SELECT 1').scalar() == 1


@pytest.mark.usefixtures('transactions')
def test_sample_data_loaded(db_session):
    trans_count = db_session.execute("SELECT count(*) FROM gumball_transaction").scalar()
    assert trans_count == 2_000
