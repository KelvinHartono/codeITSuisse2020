import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

def saladSpree(num,prices):
  def checkPrice(arr):
    temp = [(float("inf"),num)]*len(arr)
    minPrice = float("inf")
    if arr[0] == "X":
      temp[0] = (float("inf"),num)
    else:
      temp[0] = (int(arr[0]),num-1)
    for i in range(1,len(arr)):
      if arr[i]!="X":
        if temp[i-1][0]!=float("inf"):
          if temp[i-1][1]>0:
            temp[i] = (int(arr[i])+temp[i-1][0],temp[i-1][1]-1)
          elif temp[i-1][1]==0:
            temp[i] = (int(arr[i])+temp[i-1][0]-int(arr[i-num]),temp[i-1][1])
          if temp[i][1]==0:
            minPrice = min(minPrice,temp[i][0])
        else:
          temp[i] = (int(arr[i]),num-1)
      else:
        if i>len(temp)-num:
          break
        temp[i] = (float("inf"),num)
    return minPrice
  retval = float("inf")
  for x in prices:
    retval = min(checkPrice(x),retval)
  return retval if retval!=float("inf") else 0


@app.route('/salad-spree', methods=['POST'])
def salad():
  data = request.get_json()
  # logging.info("data sent for evaluation {}".format(data))
  result = saladSpree(data["number_of_salads"],data["salad_prices_street_map"])
  # logging.info("My result :{}".format(result))
  return json.dumps({'result':result})