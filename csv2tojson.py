import json
import os
import sys
from pathlib import Path
import csv
from typing import List
import bisect
import operator
from operator import attrgetter

def csv2json(methodName,filePath):

    fileList=[]
    deps = {}
    out_json = {}
    out_json["@schemaVersion"] = 1.0
    out_json["name"] = methodName
    # len1=len("django-rest-framework")
    with open(filePath, "r", encoding="utf-8") as csv_file:
        reader = csv.reader(csv_file)
        reader.__next__() 
     
        for row in reader:         
            # src = row[0][len1+1:].replace("\\", "/")
            # dest = row[1][len1+1:].replace("\\", "/")
            src = row[0]
            dest = row[1]
            count= row[2]
            if src not in fileList:
                fileList.append(src)
            if dest not in fileList:
                fileList.append(dest)
            # add_to_deps(src, dests, count,depsWS)
            if (src,dest) in deps:
                print("error 1")
            # elif (dest,src) in deps:
            #     print("error 2")
            deps[(src, dest)] =count


    cells = []
    out_json["variables"] = fileList
    for key, value in deps.items():
        # src_index = bisect.bisect_left(fileList, key[0])
        # dest_index = bisect.bisect_left(fileList, key[1])
        src_index=fileList.index(key[0])
        dest_index=fileList.index(key[1])
        if src_index != dest_index:
            an_obj = {"src": src_index, "dest": dest_index,
                      "values": {"confidence": float(value)}}
            cells.append(an_obj)
        else:
            print("error 3")
        
    cells= sorted(cells, key=lambda s:(s["src"],s["dest"]))

    out_json["cells"] = cells

    print(len(fileList))
    print(len(list(set(fileList))))
    return out_json


def CreateJson(methodName,filePath):
    json_object = csv2json(methodName,filePath)
    json_str = json.dumps(json_object, indent=4)
    filePathJson=filePath[:-4]+'.json'
    file = open(filePathJson, "w")
    file.write(json_str)
    file.close()

# CreateJson("HCP",'D:\影响分析\gajim\historyHandled.CSV')