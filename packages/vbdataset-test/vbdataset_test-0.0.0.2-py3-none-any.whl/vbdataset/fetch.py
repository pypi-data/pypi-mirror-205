import os
from datetime import datetime
from pathlib import Path

import boto3
import pymongo
from botocore.client import Config

S3 = boto3.resource('s3',
                    endpoint_url='http://172.19.221.184:9000',
                    aws_access_key_id='grai_user',
                    aws_secret_access_key='grailab12#',
                    config=Config(signature_version='s3v4'))
S3_BUCKET = S3.Bucket('vaai-body')



def download_test():
    print('download')


def create_db_by_condition(db, search_type="or", **kwargs):
    assert search_type in ['or', 'and'], "Wrong search type"

    now = datetime.now()
    dt_string = now.strftime("%Y-%m-%d-%H-%M-%S")

    filter_list = []
    for (filter_type, values) in kwargs.items():
        assert filter_type in ['file_name', 'actor', 'status', 'subject', 'is_talk'], "Wrong filtering option"
        if filter_type == 'file_name':
            filter_type = 'fileName'
        if filter_type == 'is_talk':
            filter_type = 'isTalk'
        for v in values:
            if type(v) is not str:
                pass
            filter_list.append({filter_type: v})

    bvh_download_path = Path(__file__).resolve().parent.parent.parent / 'data' / dt_string / 'bvh'
    wav_download_path = Path(__file__).resolve().parent.parent.parent / 'data' / dt_string / 'wav'
    os.makedirs(bvh_download_path)
    os.makedirs(wav_download_path)

    search_type = "$" + search_type
    for x in db.gestures.find({search_type: filter_list}):
        bvh_file_name = x['fileName'] + '.bvh'
        S3_BUCKET.download_file(x['bvhFile'], bvh_download_path / bvh_file_name)
        if x['audioFile'] is not None:
            wav_file_name = x['fileName'] + '.wav'
            S3_BUCKET.download_file(x['audioFile'], wav_download_path / wav_file_name)
