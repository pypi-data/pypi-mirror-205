import json
import os
from datetime import datetime
from pathlib import Path
from re import search
from typing import List

import boto3
import pymongo
from botocore.client import Config
from tqdm import tqdm

S3 = boto3.resource('s3',
                    endpoint_url='http://172.19.221.184:9000',
                    aws_access_key_id='grai_user',
                    aws_secret_access_key='grailab12#',
                    config=Config(signature_version='s3v4'))
S3_BUCKET = S3.Bucket('vaai-body')

MONGO = pymongo.MongoClient(host='172.19.195.104')   
GESTURE_DB = MONGO['gestureDB'] 



def fetch_db(fetch_path: str,
             actors: List[str] = ['all'], 
             gesture_types: List[str] = ['all'], 
             isTalk: bool = False,
             gesture_styles: List[str] = ['all']):
    '''
    
    Fetching data by defined conditions.

    Args:
        fetch_path (str): decide path to fetch data
        actors (List[str]): decide which actor's data to fetch.
        gesture_types (List[str]): decide which gesture type to fetch. 
        isTalk (boolean): decide whether talk or non-talk data to fetch.
        gesture_styles (List[str]): decide which gesture style to fecth.

    '''

    assert type(isTalk) == bool, "'isTalk' argument type must be boolean"

    now = datetime.now()
    dt_string = now.strftime("%Y-%m-%d-%H-%M-%S")

    conditions = '{}'
    condition_json = json.loads(conditions)

    if actors != ['all'] and len(actors) > 0:
        condition_json.update({"actor" : {"$in": actors}})

    if gesture_types != ['all'] and len(gesture_types) > 0:
        for g_type in gesture_types:
            assert g_type in ['emblem', 'manipulator', 'illustrator', 'affect display', 'regulator', 'all'], \
                        "Gesture type must be 'emblem', 'manipulator', 'illustrator', 'affect display', 'regulator' or 'all'"
        condition_json.update({"status" : {"$in": gesture_types}})

    if gesture_styles != ['all'] and len(gesture_styles) > 0:
        for g_style in gesture_styles:
            assert g_style in ['introvert', 'extrovert', 'light', 'heavy', 'slow', 'hurry', 'all'], \
                            "Gesture style must be 'introvert', 'extrovert', 'light', 'heavy', 'slow', 'hurry' or 'all'"
        condition_json.update({"style" : {"$in": gesture_styles}})

    bvh_download_path = Path(fetch_path) / dt_string / 'bvh'
    wav_download_path = Path(fetch_path) / dt_string / 'wav'
    os.makedirs(bvh_download_path)
    os.makedirs(wav_download_path)

    total_data_cnt = 0
    for x in GESTURE_DB.gestures.find({'$and': [
                                                {'isTalk': isTalk}, 
                                                condition_json
                                                ]
                                      }):
        bvh_file_name = x['fileName'] + str(x['_id']) + '.bvh'
        try:
            S3_BUCKET.download_file(x['bvhFile'], bvh_download_path / bvh_file_name)
        except Exception:
            print(f"[Error] {x['bvhFile']} is not exist")
            continue
        
        if x['audioFile'] is not None:
            wav_file_name = x['fileName'] + str(x['_id']) + '.wav'
            try:
                S3_BUCKET.download_file(x['audioFile'], wav_download_path / wav_file_name)
            except Exception:
                print(f"[Error] {x['audioFile']} is not exist")
                pass
        total_data_cnt += 1

    print(f'Data fetching complete. number of data: {total_data_cnt}')
