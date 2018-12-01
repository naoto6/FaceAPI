import http.client, urllib.request, urllib.parse, urllib.error, base64
import json
import numpy as np
import cv2
import matplotlib.pyplot as plt

#APIkey
API_KEY = "4d861fb8a8ea4c8993f17e9815347dc6"
file = "mayu.jpg"

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

try:
    conn = http.client.HTTPSConnection('japaneast.api.cognitive.microsoft.com')
    conn.request("POST", "/face/v1.0/detect?%s" % params, open(file,"rb"), headers)
    response = conn.getresponse()
    data = response.read()
    data = json.loads(data)
    emotion = RaadJson(data)
    print(emotion)
    pic = cv2.imread(file)
    pic = cv2.cvtColor(pic, cv2.COLOR_BGR2RGB)
    plt.imshow(pic)
    Recognize(emotion)
    conn.close()
except Exception as e:
    print("[Errno {0}] {1}".format(e.errno, e.strerror))
