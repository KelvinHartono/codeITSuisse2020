import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

def trace(data):
  results = []
  def diff(a,b):
    retval=0
    nonsilent=0
    for i in range(len(a)):
      if a[i]!=b[i]:
        retval+=1
        if i%4==0:
          nonsilent+=1
    return (retval,"*" if nonsilent>1 else "")

  def recurse(curr,origin,clusters,stri):
    # mindiff = min([diff(curr,cl["genome"]) for cl in clusters])
    if len(clusters)==0:
      difforigin = diff(curr,origin["genome"])
      results.append(stri+difforigin[1]+" -> "+origin["name"])
      return
    else:
      difforigin = diff(curr,origin["genome"])
      diffs = [(*diff(curr,cl["genome"]),i) for i,cl in enumerate(clusters)]
      diffs.sort(key = lambda x:x[0])
      if difforigin[0]<diffs[0][0]:
        print(difforigin[1])
        results.append(stri+difforigin[1]+" -> "+origin["name"])
      elif difforigin[0]==diffs[0][0]:
        i = 0
        recurse(curr,origin,[],stri)
        while i<len(diffs) and diffs[i][0]==diffs[0][0]:
          results.append(stri+diffs[i][1]+" -> "+clusters[diffs[i][2]]["name"])
          i+=1
      else:
        i = 0
        while i<len(diffs) and diffs[i][0]==diffs[0][0]:
          recurse(clusters[diffs[i][2]]["genome"],origin,clusters[:diffs[i][2]]+clusters[diffs[i][2]+1:],stri +diffs[i][1]+ " -> "+clusters[diffs[i][2]]["name"])
          i+=1
  recurse(data["infected"]["genome"],data["origin"],data["cluster"],data["infected"]["name"])
  return results


@app.route('/contact_trace', methods=['POST'])
def snek():
  data = request.get_json()
  logging.info("data sent for evaluation {}".format(data))
  det = trace(data)
  return jsonify(det)