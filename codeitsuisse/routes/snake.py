import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

def findMoves(data):
  bsize,numPlayers = data["boardsize"]*data["boardsize"],data["players"]
  jumpsGood = {}
  jumpsBad = {}

  def goWhere(winner,loser):
    retGood,retBad = [], []
    currMaxGood, currMaxBad = float("-inf"), float("inf")
    for i in range(1,7):
      if winner+i in jumpsGood:
        if jumpsGood[winner+i]!=0:
          retGood.append(i)
        else:
          retGood.append(i)
          retGood.append(6)
      if loser+i in jumpsGood:
        if jumpsGood[winner+i]!=0:
          retGood.append(i)
        else:
          retGood.append(i)
          retGood.append(6)
  for jump in data["jumps"]:
    temp = jump.split(":")
    temp[0],temp[1]=int(temp[0]),int(temp[1])
    if temp[0]>temp[1]:
      jumpsBad[temp[0]]=temp[1]
    else:
      jumpsGood[temp[1]]=temp[0]
  currMainCell,currOtherCell = 1,1
  while currMainCell<bsize:
    goodies,baddies=goWhere(currMainCell,currOtherCell)

@app.route('/slsm', methods=['POST'])
def snek():
  data = request.get_json()["tests"]
  logging.info("data sent for evaluation {}".format(data))
  det = findMoves(data)
  return jsonify(det)