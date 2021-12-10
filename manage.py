'''
Author : hupeng
Time : 2021/12/9 16:14 
Description: 
''' 
import json
import base64

import cv2
import numpy as np
from flask import Flask, request, Response, g
from fairy.utils import MyResponse, responser

from utils.log import rd, get_logger
import settings
from predictor import okay_cut

logger = get_logger()


def cv2_to_base64(image):
    return base64.b64encode(image).decode('utf8')


def cut_func(img):
    """
    # DB detection
    """
    data = base64.b64decode(img.encode('utf8'))
    data = np.fromstring(data, np.uint8)
    data = cv2.imdecode(data, cv2.IMREAD_COLOR)
    result = okay_cut(data)
    return result


def cut_question(image):
    # with open(image_path, 'rb') as f:
    #     img = f.read()
    # img = cv2_to_base64(img)
    result = cut_func(image)
    return result


app = Flask(__name__)


@app.before_request
def before_request():
    url = request.url
    args = request.json or request.form or {}
    requestid = request.headers.get('requestid')
    if not requestid:
        data = {'code': 10000, 'message': 'miss requestid', 'data': {}}
        return Response(
            response=json.dumps(data, ensure_ascii=False),
            mimetype='application/json'
        )

    g.requestid = requestid
    rd.requestid = requestid

    try:
        logger.info('[request] [path: %s] %s' % (request.path, str(args)))
    except Exception:
        logger.error("request url: %s, response: message too long" % url)


@app.after_request
def after_request(response):
    url = request.url
    resp = response.data.decode()
    try:
        resp = json.loads(resp)
        if resp['code'] in [10000, 10001]:
            return response
    except Exception:
        pass
    try:
        logger.info('[response] %s' % str(resp))
    except Exception:
        logger.error("request url: %s, response: message too long" % url)
    return response


@app.route('/predict/ocr_det', methods=['POST'])
def ocr_det():
    response = MyResponse()
    response.code = 0
    response.message = 'success'
    try:
        args = request.json or request.data
        imgs = args.get('images')
        result = []
        for img in imgs:
            res = cut_question(img)
            result.append(res)
        response.data = {'results': result}
    except Exception as e:
        response.code = 10001
        response.message = str(e)
    # print(response.dict)
    return responser(response)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8966, debug=False)