# -*- coding: UTF-8 -*-
# Date   : 2020/1/7 16:05
# Editor : gmj
# Desc   : 百度表格数据识别接口调用
import json
import base64
import time
import requests

""" 你的 APPID AK SK """
# APP_ID = '17092152'
# API_KEY = 'SE93T9PVjUgBbTQGfDBGkZEX'
# SECRET_KEY = 'ZfDjLzQBOerlrptRD33o9MzT9N5RzXjP'
APP_ID = '****'
API_KEY = '****'
SECRET_KEY = '****'

header = {
    'Content-Type': 'application/x-www-form-urlencoded',
}


def get_access_token():
    token_url = f'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={API_KEY}&client_secret={SECRET_KEY}&'
    res = requests.get(token_url)
    res = json.loads(res.text)
    return res['access_token']


def read_file(image_path):
    with open(image_path, 'rb') as f:
        return f.read()


def push_picture(image_path):
    access = get_access_token()
    use_image_url = f'https://aip.baidubce.com/rest/2.0/solution/v1/form_ocr/request?access_token={access}'
    image = read_file(image_path)
    encodestr = base64.b64encode(image)
    data = {'image': encodestr}
    res = requests.post(use_image_url, data=data, headers=header)
    res = json.loads(res.text)
    return res['result'][0]['request_id']


def get_result(request_id):
    access = get_access_token()
    result_url = f'https://aip.baidubce.com/rest/2.0/solution/v1/form_ocr/get_request_result?access_token={access}'
    data = {
        'request_id': request_id,
    }
    result = requests.post(result_url, data=data, headers=header)
    return result.text


def main(image_path):
    request_id = push_picture(image_path)
    time.sleep(30)
    res = get_result(request_id)
    print(res)


if __name__ == '__main__':
    my_path = './W020190623439694885213.png'
    main(my_path)
