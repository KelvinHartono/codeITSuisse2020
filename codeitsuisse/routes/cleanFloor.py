import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

def cleanFloor(data):
  # leftMost = -1
  # for index, val in enumerate(data):
  #   if val == 1:
  #     leftMost = index
  # if leftMost == -1:
  #   return 0
  curr = 1
  data[1]= data[1]-1 if data[1]>0 else data[1]+1
  step = 1
  while curr<len(data):
    print(data,step,curr)
    if data[curr-1]>0:
      data[curr-1]-=1
      if data[curr]==0 and curr==len(data)-1:
        step+=1
        break
      data[curr] = data[curr]-1 if data[curr]>0 else data[curr]+1
      step+=2
    else:
      curr+=1
      if curr>=len(data):
        break
      data[curr]= data[curr]-1 if data[curr]>0 else data[curr]+1
      step+=1
  if data[-1]>0:
    step+=data[-1]*2+1
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