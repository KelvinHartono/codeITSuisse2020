import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

def cleanFloor(data):
  curr = 1
  data[1]= data[1]-1 if data[1]>0 else data[1]+1
  step = 1
  while curr<len(data):
    if data[curr-1]>0:
      if curr == len(data)-1 and data[curr]==0:
        step-=1
      step += data[curr-1]*2
      data[curr]=data[curr]-data[curr-1]
      data[curr-1]=0
      if data[curr]<0:
        if data[curr]==-1 and curr==len(data)-1:
          step-=1
          break
        if data[curr]%2==0:
          data[curr]=0
        else:
          data[curr]=1 
    curr+=1
    if curr>len(data)-1 or (data[curr]==0 and curr==len(data)-1):
      break
    data[curr]= data[curr]-1 if data[curr]>0 else data[curr]+1
    step+=1

  if data[-1]>0:
    step+=data[-1]*2+1
  print(step)
  return step

@app.route('/clean_floor', methods=['POST'])
def clean():
  data = request.get_json()["tests"]
  logging.info("data sent for evaluation {}".format(data))
  result={'answers':{}}
  for da in data:
    ret = cleanFloor(data[da]["floor"])
    result['answers'][da] = ret
  return jsonify(result)