#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
# StringIO import StringIO
from io import StringIO,BytesIO
from email.generator import Generator

import bson
import flask
from PIL import Image # sudo apt-get install python-pil
from bson.json_util import dumps
from flask import Flask, flash, request, Response, jsonify, redirect, json
from flask_cors import CORS
from pymongo import MongoClient
from werkzeug.utils import secure_filename

import ocr

app = Flask(__name__, static_url_path="", static_folder="../web/dist/")
app.config['SECRET_KEY'] = '123456'
app.config['JSON_AS_ASCII'] = False
CORS(app) #跨域访问时使用
# 读取配置文件
app.config.from_object('config')

# 连接数据库，并获取数据库对象
db = MongoClient(app.config['DB_HOST'], app.config['DB_PORT']).test

# 将图片与图片识别结果（JSON）存入数据库
def save_file(ocrdata, file_str, fname):
    #image = StringIO(file_str)
    image = BytesIO(file_str)
    # image = file_str
    try:
        mime = Image.open(image).format.lower()
        print('image of mime is：', mime)
        if mime not in app.config['ALLOWED_EXTENSIONS']:
            raise IOError()
    except IOError:
        flask.abort(400)
    c = dict(ocrdata=ocrdata, image=bson.binary.Binary(image.getvalue()), filename=secure_filename(fname),
             mime=mime)
    #print(c)
    db.files.insert_one(c)
    return c['_id'], c['filename']

def find_model(mid):
    m = db.models.find_one(bson.objectid.ObjectId(mid))
    if m is None:
        raise bson.errors.InvalidId()
    t = json.loads(m["model"])
    return t

def find_model_list():
    list = []
    for x in db.models.find({}, {"_id":1, "name": 1}): 
        y =dict(id=str(x['_id']),label=str(x['name'])) 
        list.append(y)
    return list

def BoxStr2ArrayInt(str):
    str = str.split(',')
    box = []
    if len(str) == 8:
        box.append(int(str[0]))
        box.append(int(str[1]))
        box.append(int(str[2])-int(str[0]))
        box.append(int(str[7])-int(str[1]))
    if len(str) == 4:
        box.append(int(str[0]))
        box.append(int(str[1]))
        box.append(int(str[2]))
        box.append(int(str[3]))
    return box

def getOverlapbox(box1, box2):
    box1 = BoxStr2ArrayInt(box1)
    box2 = BoxStr2ArrayInt(box2)

    # //两个矩形在水平方向下方或上方，完全不重叠
    if (box1[1] > box2[1]+box2[3] or box1[1]+box1[3] < box2[1]) :
        return 0;
    # //两个矩形在垂直方向左侧或右侧，完全不重叠
    if (box1[0] > box2[0]+box2[2] or box1[0]+box1[2] < box2[0]) :
        return 0;
    # //重叠区域长乘宽
    side1 = 0;
    side2 = 0;
    if (box1[1]>=box2[1] and box1[1] < box2[1]+box2[3]) :
        side1 = box2[1]+box2[3] - box1[1];
    elif(box2[1]>=box1[1] and box2[1]<box1[1]+box1[3]) :
        side1 = box1[1]+box1[3] - box2[1];

    if (box1[0] >= box2[0] and box1[0]<box2[0]+box2[2]) :
        side2 = box2[0]+box2[2] - box1[0];
    elif (box2[0] >= box1[0] and box2[0]<box1[0]+box1[2]) :
        side2 = box1[0]+box1[2] - box2[2];

    return side1 * side2

def transform(ocrdata, mapping, data):
    for m in mapping['relation']:
        max = 0
        value = ''
        for region in ocrdata['regions']:
            for line in region['lines']:
                # print line['boundingBox'], m['box']
                area = getOverlapbox(line['boundingBox'], m['box'])
                if max < area:
                    max = area
                    if line.has_key('text') : 
                        value = line['text']
                    if line.has_key('lineContent'): 
                        value = line['lineContent'] 
        data['data'][m['key']] = value
        print(max, value)
    return data
# 提供接口，获取前端页面的提交的表单参数，通过调用其他文件写好的函数，获得结果，并以Json格式返回给前端页面
# @装饰器
@app.route('/api', methods=['GET', 'POST'])
def apidemo():
    return redirect('/api_test.html')

@app.route('/', methods=['GET', 'POST'])
def index():
    return redirect('/index.html')

@app.route('/api/model/<mid>', methods=['POST'])
def image2json(mid):
    #Request对象在web应用的开发中是一个非常重要的对象，主要用来获取用户发来的请求数据。
    if request.method == 'POST':
        if mid == 0 or mid is None:
            return jsonify({"error": "No selected model"}) 
        print(request)
        if 'file' not in request.files:
            flash('No file part')
            return jsonify({"error": "No file part"})
        imgfile = request.files['file']
        if imgfile.filename == '':
            flash('No selected file')
            return jsonify({"error": "No selected file"})
        if imgfile:
            file_str = imgfile.read()
            ocrdata = ocr.ocr(file_str)
            fid, filename = save_file(ocrdata, file_str, imgfile.filename)
            print('fid:', fid)
            if fid is not None:
                model = find_model(mid)
                ocrdata = json.loads(ocrdata)
                model['DataModel'] = transform(ocrdata['Result'], model['mapping'], model['DataModel'])
            return Response(json.dumps(model['DataModel']), mimetype='application/json')
    return jsonify({"error": "No POST methods"})

@app.route('/uploadUrl/<mid>', methods=['POST'])
def upload(mid):
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return jsonify({"error": "No file part"})
        imgfile = request.files['file']
        if imgfile.filename == '':
            flash('No selected file')
            return jsonify({"error": "No selected file"})
        if imgfile:
            file_str = imgfile.read()
            ocrdata = ocr.ocr(file_str)
            #print(ocrdata)
            fid, filename = save_file(ocrdata, file_str, imgfile.filename)
            print('fid:', fid)
            if fid is not None:
                ocrdata = json.loads(ocrdata)
                if mid != '0' and mid is not None:
                    model = find_model(mid)
                    model['DataModel'] = transform(ocrdata['Result'], model['mapping'], model['DataModel'])
                else:
                    model = {
                        'DataModel': {
                             'data': {
                                "default":"value"
                            }
                        },
                        'mapping': {
                            "relation": []
                        } 
                    }
                data = {
                        "fid": str(fid),
                        "filename": str(filename),
                        "ocrdata": ocrdata,
                        "model": model
                }
            return Response(json.dumps(data), mimetype='application/json')
    return jsonify({"error": "No POST methods"})

@app.route('/saveDataModel', methods=['POST'])
def saveDataModel():
    if request.method == 'POST':
        print(request.data)
        req = request.data #.decode("gb2312")
        req = json.loads(request.data)
        print(req)
        data = dict(name=req['name'], model=request.data)
        db.models.save(data);
        list = find_model_list()
        return Response(json.dumps({"dataModelList": list}), mimetype='application/json')
    return jsonify({"error": "No POST methods"})

@app.route('/getDataModelList')
def getDataModelList():
    try:
        list = find_model_list()
        return Response(json.dumps({"dataModelList": list}), mimetype='application/json')
    except bson.errors.InvalidId:
        flask.abort(404)

@app.route('/models/<mid>')
def getDataModel(mid):
    try:
        t = find_model(mid)
        return Response(json.dumps(t), mimetype='application/json')
    except bson.errors.InvalidId:
        flask.abort(404)

@app.route('/rm_models/<mid>')
def rmDataModel(mid):
    try:
        t = db.models.delete_one({"_id":bson.objectid.ObjectId(mid)})
        return Response(str(t.deleted_count) + " files deleted!")
    except bson.errors.InvalidId:
        flask.abort(404)

'''
    根据图像oid，在mongodb中查询，并返回Binary对象
'''
@app.route('/file/<fid>')
def find_file(fid):
    try:
        file = db.files.find_one(bson.objectid.ObjectId(fid))
        if file is None:
            raise bson.errors.InvalidId()
        return Response(file['image'], mimetype='image/' + file['mime'])
    except bson.errors.InvalidId:
        flask.abort(404)


'''
    直接从数据库中取出之前识别好的JSON数据，并且用bson.json_util.dumps将其从BSON转换为JSON格式的str类型
'''
@app.route('/ocrjson/<fid>')
def get_ocrjson(fid):
    # print 'get_report(fid):', fid
    try:
        file = db.files.find_one(bson.objectid.ObjectId(fid))
        if file is None:
            raise bson.errors.InvalidId()
        ocrdata = json.loads(file['ocrdata'])
        return jsonify(ocrdata)
    except bson.errors.InvalidId:
        flask.abort(404)

    
if __name__ == '__main__':
    app.run(host=app.config['SERVER_HOST'], port=app.config['SERVER_PORT'])
    # model = find_model("603708ddc8a9f5fdb97dad15")
    # file = db.files.find_one(bson.objectid.ObjectId("6037cb3fbdafd7c59a62d18f"))
    # ocrdata = json.loads(file['ocrdata'])
    # m = dict(key="default",box="31,140,106,140,106,158,31,158")
    # list = []
    # list.append(m) 
    # mapping = dict(relation=list)
    # print transform(ocrdata['Result'], mapping, model['DataModel'])
    
