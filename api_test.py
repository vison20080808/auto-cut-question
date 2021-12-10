'''
Author : hupeng
Time : 2021/12/10 14:08 
Description: 服务接口测试脚本
'''
import json
import base64
import argparse

import cv2
import requests


def main(args):
    url = f'http://{args.host}:{args.port}/api/detect/question_segment'
    headers = {"Content-type": "application/json", "requestid": "api_test"}
    img = cv2.imread(args.image_path)
    data = cv2.imencode('.jpg', img)[1]
    image_bytes = data.tobytes()
    image_base4 = base64.b64encode(image_bytes).decode('utf8')
    data = {'images': [image_base4]}
    res = requests.post(
        url=url,
        data=json.dumps(data),
        headers=headers
    ).json()
    print(res['data']['results'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', type=str, default='127.0.0.1')
    parser.add_argument('--port', type=int, default=8977)
    parser.add_argument('--image_path', type=str, default='test/IMG_20211022_145648.jpg')
    args = parser.parse_args()
    main(args)
