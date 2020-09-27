import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

def findMoves(data):
  bsize,numPlayers = data["boardSize"],data["players"]
  jumpsGood = {}
  jumpsBad = {}
  for jump in data["jumps"]:
    temp = jump.split(":")
    temp[0],temp[1]=int(temp[0]),int(temp[1])
    if temp[0]>temp[1]:
      jumpsBad[temp[0]]=temp[1]
    else:
      if temp[0]==0:
        jumpsGood[temp[1]]=temp[0]
      else:
        jumpsGood[temp[0]]=temp[1]
  currMainCell= 1
  moves =[]
  while currMainCell<bsize:
    print(currMainCell,"-",end="")
    if bsize-currMainCell<=6:
      for _ in range(numPlayers-1):
        for i in range(1,7):
          if i+currMainCell not in jumpsGood and i+currMainCell not in jumpsBad and i+currMainCell!=bsize:
            moves.append(i)
            break
      moves.append(bsize-currMainCell)
      currMainCell+=bsize-currMainCell
      break
    bestMove=(6,currMainCell+6,False)
    stay = False
    for i in range(1,7):
      if currMainCell+i in jumpsGood:
        if jumpsGood[currMainCell+i]!=0 and jumpsGood[currMainCell+i]>bestMove[1]:
          bestMove=(i,jumpsGood[currMainCell+i],True)
          stay = False
        # elif jumpsGood[currMainCell+i]==0 and currMainCell+i+1>bestMove[1]:
        #   bestMove = (i,currMainCell+i+1,False)
        #   stay = True
      elif currMainCell+i in jumpsBad:
        continue
      else:
        if i+currMainCell>bestMove[1]:
          bestMove=(i,i+currMainCell,False)
    for _ in range(numPlayers):
      moves.append(bestMove[0])
    currMainCell = currMainCell+bestMove[0]
    if bestMove[2]:
      currMainCell = bestMove[1]
    if stay==True:
      print("hell naw")
  print(jumpsGood,jumpsBad)
  print(currMainCell,len(moves))
  return moves

            
@app.route('/slsm', methods=['POST'])
def sneik():
  data = request.get_json()
  logging.info("data sent for evaluation {}".format(data))
  det = findMoves(data)
  return jsonify(det)