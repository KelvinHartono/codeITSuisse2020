import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

def saladSpree(num,prices):
  def checkPrice(arr):
    minPrice = float("inf")
    if arr[0] == "X":
      arr[0] = (float("inf"),num)
    else:
      arr[0] = (int(arr[0]),num-1)
    for i in range(1,len(arr)):
      if arr[i]!="X":
        if arr[i-1][0]!=float("inf"):
          arr[i] = (int(arr[i])+arr[i-1][0],arr[i-1][1]-1)
          if arr[i][1]==0:
            minPrice = min(minPrice,arr[i][0])
        else:
          arr[i] = (int(arr[i]),num-1)
      else:
        if i>len(arr)-num:
          break
        arr[i] = (float("inf"),num)
    return minPrice
  retval = float("inf")
  for x in prices:
    retval = min(checkPrice(x),retval)
  return retval if retval!=float("inf") else 0


@app.route('/salad-spree', methods=['POST'])
def salad():
  data = request.get_json()
  logging.info("data sent for evaluation {}".format(data))
  result = saladSpree(data["number_of_salads"],data["salad_prices_street_map"])
  logging.info("My result :{}".format(result))
  return json.dumps({'result':result})