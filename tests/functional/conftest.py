import datetime
import pathlib

import botocore.exceptions
import more_itertools as mi
import collections
import csv
import typing

import pytest
import requests
import sqlalchemy
import sqlalchemy.orm

import opshub
import opshub.fileshare
from opshub import models


@pytest.fixture(name='file_share', scope='session')
def _file_share(app):
    """boto s3 client object"""
    s3 = opshub.fileshare.create_client(app)

    try:
        res = s3.list_buckets()
        assert res['ResponseMetadata']['HTTPStatusCode'] == 200
    except botocore.exceptions.BotoCoreError:
        pytest.fail('Unable to connect to S3 service (hint: try docker-compose up)')
        return
    buckets = [r['Name'] for r in res['Buckets']]

    bucket_name = app.config.get('S3_BUCKET_NAME')

    if bucket_name not in buckets:
        s3.create_bucket(ACL='public-read-write', Bucket=bucket_name)
    return s3


@pytest.fixture(name='bucket_dir', scope='session')
def _bucket_dir(file_share, app):
    """Local directory where s3 bucket objects are stored"""
    p = pathlib.Path(__file__).parent.parent.parent / 'data' / app.config.get('S3_BUCKET_NAME')
    if not p.exists():
        pytest.fail(f'Local directory for S3 service not found: {p}')
    return p


@pytest.fixture(name='app', scope='session')
def _app():
    """Flask app instance spun up in separate process.  Runs on localhost:5000"""
    import multiprocessing
    app = opshub.create_app()

    def run():
        app.run('0.0.0.0')

    d = multiprocessing.Process(target=run)
    d.start()

    assert requests.get('http://localhost:5000/').status_code == 200
    yield app
    d.terminate()


@pytest.fixture(name='db_session', scope='session')
def _db_session(app) -> sqlalchemy.orm.Session:
    """
    Database session to use in tests.

    Note, DB schema is completely dropped and re-created at the beginning of
    each test session.
    """
    e = sqlalchemy.create_engine(app.config.get('SQLALCHEMY_DB_URL'))
    models.Base.metadata.drop_all(e)
    models.Base.metadata.create_all(e)

    sess = sqlalchemy.orm.Session(bind=e)
    yield sess
    sess.close()


@pytest.fixture(name='transactions', scope='session')
def _transactions(db_session):
    """Load a sample of transactions for several gumball machines"""

    test_data_path = pathlib.Path(__file__).parent.parent / 'fixtures/transactions.txt'

    db_session.query(models.GumballTransaction).delete()
    db_session.commit()

    for i in range(6):
        db_session.add(models.GumballMachine(serial_no=f'GM00{i + 1}'))
    db_session.commit()

    def _load_all(
            transactions: typing.Iterable[typing.Tuple[str, str, str]]
    ) -> typing.Iterable[models.GumballTransaction]:
        trans_ids = collections.Counter()
        for sn, td, dc in transactions:
            trans_ids[sn] += 1
            try:
                yield models.GumballTransaction(
                    trans_id=trans_ids[sn],
                    serial_no=sn,
                    trans_date=datetime.datetime.strptime(td, '%Y-%m-%dT%H:%M:%SZ'),
                    dispense_count=int(dc))
            except ValueError as ve:
                raise ve

    with test_data_path.open() as f:
        reader = csv.DictReader(f, ('serial_no', 'transaction_date', 'dispense_count'), delimiter='|')
        rows = sorted(reader, key=lambda r: r['transaction_date'])
        for chunk in mi.chunked(_load_all((r.values() for r in rows)), 200):
            db_session.add_all(chunk)
            db_session.commit()
