import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

def saladSpree(num,prices):
  def checkPrice(arr):
    minPrice = float("inf")
    temp = [(float("inf"),num)]*len(arr)
    for i in range(len(arr)):
      if arr[i]!="X":
        if temp[i-1][0]!=float("inf"):
          temp[i] = (int(arr[i])+temp[i-1][0],temp[i-1][1]-1)
          if temp[i][1]==0:
            minPrice = min(minPrice,temp[i][0])
        else:
          temp[i] = (int(arr[i]),num-1)
    return minPrice
  retval = min([checkPrice(x) for x in prices])
  return retval if retval!=float("inf") else 0


@app.route('/salad-spree', methods=['POST'])
def salad():
  data = request.get_json()
  logging.info("data sent for evaluation {}".format(data))
  result = saladSpree(data["number_of_salads"],data["salad_prices_street_map"])
  logging.info("My result :{}".format(result))
  return json.dumps(result)