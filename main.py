import argparse
# from typing_extensions import ParamSpec
import handlehistory
import csv2tojson
import hcp
import AssociationRule
import follow
import Distance




parser = argparse.ArgumentParser(description='111')
parser.add_argument('--filePath',type=str,default=None)
parser.add_argument('--method',type=str,default=None)
parser.add_argument('--support',type=int,default=None)
parser.add_argument('--confidence',type=float,default=None)
parser.add_argument('--IndexDistance',type=int,default=None)
parser.add_argument('--TimeDistance',type=int,default=None)
args=parser.parse_args()


csvFilePath=""
#处理commit history

if args.method=='HCP':
    historyHandled=handlehistory.first_handle(args.filePath)
    csvFilePath=hcp.GetCochange(historyHandled,args.support,args.confidence)
    csv2tojson.CreateJson("HCP",csvFilePath)
elif args.method=='follow':
    csvFilePath=follow.GetCochange(args.filePath,args.support,args.confidence)
    csv2tojson.CreateJson("follow",csvFilePath)
elif args.method=='Distance':
    historyHandled=handlehistory.first_handle(args.filePath)
    csvFilePath=Distance.GetCochange(historyHandled,args.support,args.confidence,args.IndexDistance,args.TimeDistance)
    csv2tojson.CreateJson("Distance",csvFilePath)
elif args.method=='AssociationRules':
    historyHandled=handlehistory.first_handle(args.filePath)
    csvFilePath=AssociationRule.GetCochange(historyHandled,args.support,args.confidence)
    csv2tojson.CreateJson("AssociationRule",csvFilePath)
else:
    print("请选择正确的方法！")




