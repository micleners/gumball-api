"""
OpsHub

"""
from flask import request
from flask_cors import CORS
import botocore
import boto3
import os
from flask import Flask
from opshub.fileshare import create_client
from opshub import s3_helpers

version = '0.0.1'


def create_app(*args, **kwargs) -> Flask:
    app = Flask(__name__, *args, **kwargs)
    app.config.from_pyfile('config.py')
    cors = CORS(app, resources={r"*": {"origins": ["http://localhost:3000", "http://localhost:8000", "https://gsi.micleners.com"]}})

    bucket_name = app.config.get('S3_BUCKET_NAME')

    @app.route('/upload', methods=['POST'])
    def upload():
        if request.method == "POST":
            f = request.files['file']

            # give specific bad request if this isn't provided
            tech_id = request.form['technician-id']

            # give specific bad request if this isn't provided
            mach_id = request.form['machine-id']
            s3 = create_client(app)

            response = s3_helpers.upload_file(
                s3, bucket_name, f, tech_id, mach_id)
            return str(response)

    @app.route('/uploads')
    def get_uploads():
        if request.method == "GET":
            tech_id = request.args['technician-id']
            s3 = create_client(app)

            files = s3_helpers.get_file_names(s3, bucket_name, tech_id)

            return {'files': files, 'technician_id': tech_id}

    @app.route('/')
    def home():
        s3 = create_client(app)
        return "apples"

    return app
