import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;
import random
logger = logging.getLogger(__name__)

def fruity(data):
  i = 0
  res = 0
  for el in data:
    x = random.randint(0,1000)
    logging.info(f"{i} : {x}")
    res+=x*data[el]
  return res

@app.route('/fruitbasket', methods=['POST'])
def fruit():
  data = request.get_json()["tests"]
  logging.info("data sent for evaluation {}".format(data))
  return json.dump(fruity(data))