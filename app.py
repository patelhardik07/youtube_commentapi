from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import requests
import json
from googleapiclient.discovery import build
from langdetect import detect 

app = Flask(__name__)
CORS(app)
cors = CORS(app, resources={
    r"/*": {
        "origins": "*"
    }
})
# routes
@app.route('/', methods=['POST'])
#@crossdomain(origin='*')
def predict():
  data = request.get_json(force=True)
  res={}
  api_key = "AIzaSyCRTuHl7Q-H_gJO1scbBtWVazqLkS6rp2o"
  youtube=build('youtube','v3',developerKey=api_key)
  videoid = data['videoid']
  vid_res = youtube.videos().list(part='snippet',id=videoid).execute() 
  comments=[]
  nextPage_token=None
  while 1:
    req_comment=youtube.commentThreads().list(part='snippet',videoId=videoid, maxResults=100, pageToken=nextPage_token).execute()
    nextPage_token=req_comment.get('nextPageToken')
    for item in req_comment['items']:
      comments.append(item['snippet']['topLevelComment']['snippet']['textOriginal'])
    if nextPage_token is None:
      break 
  
  hindicmt=[]
  for ctt in comments:
    try:
      lang = detect(ctt)
    except:
      language = "error"
    if (lang=='hi'):
      hindicmt.append(ctt)
  
  res['comment']={}
  i=0
  for h in hindicmt:
    res['comment'][i]=h
    i+=1
  return jsonify(res)
if __name__ == "__main__":
    app.run(port = 5000, debug=True)
