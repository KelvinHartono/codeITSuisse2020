import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;
import math
import numpy as np
logger = logging.getLogger(__name__)

@app.route('/optimizedportfolio', methods=['POST'])
def evaluate_optimizeportfolio():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    result = []
    for testcase in data["inputs"]:
        result.append(optimizeportfolio(testcase["Portfolio"], testcase["IndexFutures"]))
    logging.info("My result :{}".format(result))
    return json.dumps({"outputs":result})
    
def round_integer(num):
    roundedNum = round(num)
    if num >= roundedNum+0.5:
        roundedNum += 1
    return roundedNum

def round_decimal(num, k):
    roundedNum = round(num, 3)
    if num >= roundedNum+0.0005:
        roundedNum += 0.001
    return roundedNum

def optimizeportfolio(portfolio, indexFutures_list):
    spotPrcVol = portfolio["SpotPrcVol"]
    idx = 0
    minVol = float("inf")
    minNumContract = float("inf")
    optimalHedgeRatio = float("inf")
    indexFutures = np.array(indexFutures_list) 
    for i in range(len(indexFutures)):
        hedgeRatio = indexFutures[i]["CoRelationCoefficient"] * (spotPrcVol/indexFutures[i]["FuturePrcVol"])
        roundedHedgeRatio = round_decimal(hedgeRatio, 3)
        numContract = round_integer(roundedHedgeRatio * portfolio["Value"] / (indexFutures[i]["IndexFuturePrice"]*indexFutures[i]["Notional"]))
        if  hedgeRatio <= optimalHedgeRatio:
          if hedgeRatio == optimalHedgeRatio and indexFutures[i]["FuturePrcVol"] <= minVol:
            if indexFutures[i]["FuturePrcVol"] == minVol:
              if numContract < minNumContract:
                idx = i
                minVol = indexFutures[i]["FuturePrcVol"]
                optimalHedgeRatio = hedgeRatio
                minNumContract = numContract
            else:
              idx = i
              minVol = indexFutures[i]["FuturePrcVol"]
              optimalHedgeRatio = hedgeRatio
              minNumContract = numContract
          else:
            idx = i
            minVol = indexFutures[i]["FuturePrcVol"]
            optimalHedgeRatio = hedgeRatio
            minNumContract = numContract
        elif hedgeRatio >= optimalHedgeRatio:
            continue
    print(minNumContract)
    result = {"HedgePositionName": indexFutures[idx]["Name"], "OptimalHedgeRatio": round_decimal(optimalHedgeRatio, 3), "NumFuturesContract": minNumContract}
    return result