import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

def socialDistance(data):
  seats,people,spaces = data['seats'],data['people'],data['spaces']
  memoize = {}
  def recurse(s,p,sp,maxSeats):
    if (s,p) in memoize:
      return memoize[(s,p)]
    if p==0:
      return 1
    elif s>=maxSeats:
      return 0
    else:
      ret = 0
      for i in range(s,maxSeats):
        if i>=maxSeats:
          continue
        ret+=recurse(i+sp+1,p-1,sp,maxSeats)
      memoize[(s,p)]=ret
      return ret
  res = 0
  for i in range(seats):
    res+=recurse(i+spaces+1,people-1,spaces,seats)
  return res

@app.route('/social_distancing', methods=['POST'])
def social():
  data = request.get_json()["tests"]
  logging.info("data sent for evaluation {}".format(data))
  result={'answers':{}}
  for da in data:
    ret = socialDistance(data[da])
    result['answers'][da] = ret
  return jsonify(result)