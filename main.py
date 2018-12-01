#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, redirect, url_for,send_from_directory

from werkzeug import secure_filename
from datetime import datetime
import os

import http.client, urllib.request, urllib.parse, urllib.error, base64
import json
import numpy as np
from PIL import Image
#import matplotlib.pyplot as plt

# 自身の名称を app という名前でインスタンス化する
UPLOAD_FOLDER ="./static/images/"
app = Flask(__name__)
app.config['DEBUG'] = True
ALLOWED_EXTENSIONS = set(['png', 'jpg'])


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


#APIkey
API_KEY = "4d861fb8a8ea4c8993f17e9815347dc6"


def RaadJson(datas):
  emotion = []
  emo = ["anger","contempt","disgust","fear","happiness","sadness","surprise"]
  #anger, contempt, disgust, fear, happiness, sadness and surprise.
  for data in datas:
    #
    f = data["faceAttributes"]
    d = f["emotion"]
    for name in emo:
      emotion.append(d[name])
  return emotion


def Recognize(emotion):
    data = np.array(emotion)
    emo = np.array(["怒り","悔しい","嫌","恐怖","幸せ","悲しい","驚く"])
    num = np.argmax(data)
    pred = "この写真は「" +emo[num] + "」という感情です"
    print(pred)
    return pred

headers = {
 # Request headers
    'Content-Type': 'application/octet-stream',
    'Ocp-Apim-Subscription-Key': API_KEY,
    }

params = urllib.parse.urlencode({
    # Request parameters
    'returnFaceId': 'false',
    'returnFaceLandmarks': 'false',
    'returnFaceAttributes': 'emotion'
    })

# ルーティング。/にアクセス時
@app.route('/', methods=['GET', 'POST'])
def upload():
    if request.method == 'GET':
        return render_template('index.html')
    if request.method == 'POST':
       # アプロードされたファイルを保存する
       f = request.files['file']
       
       if f and allowed_file(f.filename):
       
            filename =secure_filename(f.filename)
       
            filepath = UPLOAD_FOLDER + filename
           
            f.save(filepath)

            try:
                conn = http.client.HTTPSConnection('japaneast.api.cognitive.microsoft.com')
                conn.request("POST", "/face/v1.0/detect?%s" % params, open(filepath,"rb"), headers)
                response = conn.getresponse()
                data = response.read()
                data = json.loads(data)
                emotion = RaadJson(data)
                print(emotion)
                #pic = cv2.imread(file)
                #pic = cv2.cvtColor(pic, cv2.COLOR_BGR2RGB)
                pic = Image.open(filepath)
                #plt.imshow(pic)
                pred = Recognize(emotion)
                conn.close()
            except Exception as e:
                print("[Errno {0}] {1}".format(e.errno, e.strerror))
                
            return render_template('index.html', filepath = filepath , predict = pred )
       
       else:
           return render_template('index.html',message='許可されていない拡張子です')
        
    else:
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run("0.0.0.0") # どこからでもアクセス可能に
