import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

def inv(item,datas):
  def minDistance(word1, word2):
    m = len(word1)
    n = len(word2)
    word1temp = word1.lower()
    word2temp = word2.lower()
    table = [[(0,"")] * (n + 1) for _ in range(m + 1)]
    temp = ""
    for i in range(m + 1):
      if i>0:
        temp+="-"+word1[i-1]
      table[i][0] = (i,temp)
    temp = ""
    for j in range(n + 1):
      if j>0:
        temp+="-"+word2[j-1]
      table[0][j] = (j,temp)
    for i in range(1, m + 1):
      for j in range(1, n + 1):
        if word1temp[i - 1] == word2temp[j - 1]:
          table[i][j] = (table[i - 1][j - 1][0],table[i - 1][j - 1][1]+word1[i-1])#"N"
        else:
          if table[i - 1][j][0]<=table[i][j - 1][0] and table[i - 1][j][0]<=table[i - 1][j - 1][0]:
            table[i][j] = (table[i - 1][j][0]+1,table[i - 1][j][1]+"-"+word1[i - 1])#"A"
          elif table[i][j - 1][0]<=table[i - 1][j][0] and table[i][j - 1][0]<=table[i - 1][j - 1][0]:
            table[i][j] = (table[i][j - 1][0]+1,table[i][j - 1][1]+"+"+word2[j - 1])#"D"
          elif table[i - 1][j - 1][0]<=table[i][j - 1][0] and table[i - 1][j - 1][0]<=table[i - 1][j][0]:
            table[i][j] = (table[i - 1][j - 1][0]+1,table[i - 1][j - 1][1]+word2[j - 1])#"R"
    return [*table[-1][-1],word2]
  res = [minDistance(item,x) for x in datas]
  res.sort(key = lambda x:(x[0],x[2].lower()))
  if len(res)>10:
    return [item[1] for item in res[:10]]
  else: 
    return [item[1] for item in res] 

@app.route('/inventory-management', methods=['POST'])
def inventory():
  data = request.get_json()
  logging.info("data sent for evaluation {}".format(data))
  result=[]
  for da in data:
    res = {}
    res["searchItemName"]=da["searchItemName"]
    res["searchResult"]=inv(da["searchItemName"],da["items"])
    result.append(res)
  ret = json.dumps(result)
  return ret