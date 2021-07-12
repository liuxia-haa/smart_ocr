# -*- coding: utf-8 -*-
import sys
import uuid
import requests
import base64
import hashlib
import time

#reload(sys)
#sys.setdefaultencoding('utf-8')

YOUDAO_URL = 'https://openapi.youdao.com/ocrapi'
APP_KEY = '0e3a5feeba404dd1'
APP_SECRET = 'yLqdlGnshiUrjsscr8QomPBjLOY8xTBx'


def truncate(q):
    if q is None:
        return None
    q_utf8 = q.decode("utf-8")
    size = len(q_utf8)
    return q_utf8 if size <= 20 else q_utf8[0:10] + str(size) + q_utf8[size - 10:size]


def encrypt(signStr):
    hash_algorithm = hashlib.sha256()
    hash_algorithm.update(signStr.encode('utf-8'))
    return hash_algorithm.hexdigest()


def do_request(data):
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    return requests.post(YOUDAO_URL, data=data, headers=headers)


def ocr(img):
    q = base64.b64encode(img)  # 读取文件内容，转换为base64编码
    data = {}
    data['detectType'] = '10012'
    data['imageType'] = '1'
    data['langType'] = 'auto'
    data['img'] = q
    data['docType'] = 'json'
    data['signType'] = 'v3'
    curtime = str(int(time.time()))
    data['curtime'] = curtime
    salt = str(uuid.uuid1())
    signStr = APP_KEY + truncate(q) + salt + curtime + APP_SECRET
    sign = encrypt(signStr)
    data['appKey'] = APP_KEY
    data['salt'] = salt
    data['sign'] = sign

    response = do_request(data)
    return response.content


if __name__ == '__main__':
    f = open(r'../pictures/1.png', 'rb')  # 二进制方式打开图文件
    img = f.read()
    f.close()
    ocrdata = ocr(img)
    print(ocrdata)