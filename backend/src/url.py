from flask import Blueprint, request
import requests
from PIL import Image
import numpy as np
import boto3
from botocore.exceptions import ClientError
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path="../.env")

s3_client = boto3.client('s3', aws_access_key_id=os.getenv('AWS_ACCESS_KEY'),
    aws_secret_access_key=os.getenv('AWS_SECRET_KEY'),
    region_name=os.getenv('AWS_REGION_NAME'))


bp = Blueprint('url', __name__, url_prefix='/yo')


@bp.route('/', methods=['POST'])
def link_submit():
   data = request.json
   print(data)
   img_data = requests.get(data['url']).content
   ext = find_extension(data['url'])
   with open(f"preprocessed/{data['name']}{ext}", 'wb') as handler:
        handler.write(img_data)
        return {'success':True}, 200, {'ContentType':'application/json'}
   
@bp.route('/batch-process', methods=['GET'])
def batch_process():
    file_names = os.listdir('preprocessed')
    try:
        for thing in file_names:
            im = Image.open(f"preprocessed/{thing}")
            print(im.getbbox())
            im2 = im.crop(im.getbbox()) 
            im2.save(f"postprocessed/{thing}")
    except:
        return {'success':False}, 400, {'ContentType':'application/json'}
    return {'success':True}, 200, {'ContentType':'application/json'}


@bp.route('/batch-upload', methods=['GET'])
def batch_upload():
    file_names = os.listdir('postprocessed')
    try:
        for thing in file_names:
            path = f"postprocessed/{thing}"
            upload_file(path, thing)
    except:
        return {'success':False}, 400, {'ContentType':'application/json'}
    return {'success':True}, 200, {'ContentType':'application/json'}

def find_dot(slug):
    dot = 0
    for index in reversed(range(0, len(slug))):
        if slug[index] == '.':
            dot = index
            break
    return dot
   

def find_extension(slug):
    return slug[find_dot(slug):]

def upload_file(file_path, file_name):
    try:
        response = s3_client.upload_file(file_path, os.getenv('AWS_BUCKET_NAME'), f"logos/bot/{file_name}")
        print(response)
    except ClientError as e:
        print(e)
        return False
    return True
    