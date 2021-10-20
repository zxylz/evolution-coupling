#删除了master中删除的文件

from os import supports_bytes_environ
import re
import csv 
from collections import namedtuple
from datetime import datetime, timezone
import collections
class commitModel(object):
    def __init__(self,id,time,index):
        self.id = id
        self.time = time
        self.index = index
    def prCommit(self):
        print("id:"+self.id+"time:"+self.time+"index:"+self.index)
    def getId(self):
        return self.id
    def getTime(self):
        return self.time
    def getIndex(self):
        return self.index
class filePair(object):
    def __init__(self,file1,file2,count):
        self.file1 = file1
        self.file2 = file2
        self.count = count
    def prFilePair(self):
        print("file1:"+self.file1+"  file2:"+self.file2+"  count:"+self.count)
    def getFile1(self):
        return self.file1
    def getFile2(self):
        return self.file2  
    def getCount(self):
        return self.count 
class commitPair(object):
    def __init__(self,commit1,commit2):
        self.commit1 = commit1
        self.commit2 = commit2
    def getcommit1(self):
        return self.commit1
    def getcommit2(self):
        return self.commit2        
    def equals(self,OnecommitPair):
        if self.commit1.getId() == OnecommitPair.getcommit1().getId():
            if  self.commit2.getId() == OnecommitPair.getcommit2().getId():                
                return True
            else:               
                return False
        elif self.commit1.getId() == OnecommitPair.getcommit2().getId():
            if  self.commit2.getId() == OnecommitPair.getcommit1().getId():               
                return True  
            else:              
                return False
        else:      
            return False           
#将txt中数据存入列表

#设置阈值
# CommitDistance = int(input("CommitDistance:"))
# TimeDistance = int(input("TimeDistance:"))
# Threshold = int(input("Threshold:"))
CommitDistance=0
TimeDistance=0
support=0
confidence=0.0
# Threshold=0
# Threshold2=0.0

cochanges=[]
fileChange={}
fileList=[]
MoreFileCommit=[]


def GetMoreFileList(filePath):

    global MoreFileCommit
    file = open(filePath,'r',encoding='UTF-8')
    matchPattern11 = re.compile(r'(^commit)')
    matchPattern21 = re.compile(r'(^M)|(^A)|(^R)|(^D)')
    
    fileOneCimmit=0

    beforeCommit=''
    for line in file.readlines():

        if matchPattern11.search(line):   #如果commit和time行
            if fileOneCimmit >10:
                MoreFileCommit.append(beforeCommit)
            tmp = line.strip('\n').split(' ',2)[1]
            id = tmp.split('(',2)[0]
            beforeCommit=id
            # time = tmp.split('(',2)[1]+' '+line.strip('\n').split(' ',3)[2]
            # time = time.replace(')','')
            fileOneCimmit=0
            # print(time)
        if matchPattern21.search(line):   #如果时文件信息行M 或A
            fileOneCimmit=fileOneCimmit+1


    #最后一个commit
    if fileOneCimmit>10:
        MoreFileCommit.append(beforeCommit)

    file.close()
    print("len(moreCommit)；"+str(len(MoreFileCommit)))
    return MoreFileCommit

def handleHistory(filePath):
    global fileChange,fileList
    file = open(filePath,'r',encoding='UTF-8')

    DelFileNum=0
    matchPattern1 = re.compile(r'(^commit)')
    matchPattern2 = re.compile(r'(^M)|(^A)')
    matchPattern3 = re.compile(r'(^R)')
    matchPattern4 = re.compile(r'(^\d)')
    matchPattern5 = re.compile(r'(^A)')
    # matchPattern6 = re.compile(r'(_$)')
    matchPattern7 = re.compile(r'(^D)')


    tmp=""
    id=""
    time=""
    index="" 

    
    for line in file.readlines():
        

        if matchPattern1.search(line):   #如果commit和time行
            tmp = line.strip('\n').split(' ',2)[1]
            id = tmp.split('(',2)[0]
            time = tmp.split('(',2)[1]+' '+line.strip('\n').split(' ',3)[2]
            time = time.replace(')','')
            # print(time)
            
        if matchPattern4.search(line):   #如果index行
            index = line
        if matchPattern2.search(line):   #如果时文件信息行M 或A
            commit= commitModel(id,time,index)
            fileName = line.strip('\n').split('	',2)[1]
            # print("fileName:"+fileName)
            if fileName in fileChange.keys():
                commitList=[]
                commitList = fileChange[fileName]
                commitList.append(commit)
                fileChange[fileName] = commitList
            else:
                commitList = []
                commitList.append(commit)
                fileChange[fileName] = commitList
                fileList.append(fileName)
        if matchPattern3.search(line):   #如果时文件信息行R
            commit= commitModel(id,time,index)
            fileName = line.strip('\n').split()[1]
            fileNewName = line.strip('\n').split()[2]


            if fileName in fileChange.keys():      #没有考虑fileNewName也在commitList中的情况   fileNewName本来就存在，其他的又重命名为了 fileNewName，这种情况有可能是因为在handlwhistory时，因为超过阈值10去掉了commit
                # print("执行了")
                commitList = []
                commitList = fileChange.pop(fileName)
                commitList.append(commit)
                
                if fileNewName in fileChange.keys():              
                    fileChange[fileNewName]=commitList+fileChange[fileNewName]
                    fileList.remove(fileName)
                else:
                    fileChange[fileNewName]=commitList
                    fileList.remove(fileName)
                    fileList.append(fileNewName)

            else:
                print(fileName)
                commitList = []
                commitList.append(commit)
                if fileNewName in fileChange.keys():
                    fileChange[fileNewName]=commitList+fileChange[fileNewName]
                else:
                    fileChange[fileNewName]=commitList
                    fileList.append(fileNewName)

        if matchPattern7.search(line):
            DelFileNum=DelFileNum+1
            fileName = line.strip('\n').split('	',2)[1]
            if fileName in fileChange.keys():
                fileChange.pop(fileName)
            if fileName in fileList:
                fileList=list(set(fileList))
                fileList.remove(fileName)
                # fileListTmp=fileList[:]
                # #避免fileList中有重复
                # for i in fileListTmp:
                #     if i==fileName:
                #         fileListTmp.remove(i)
                # fileList=fileListTmp[:]     
    file.close()
  
    print(DelFileNum)
    print("len(fileChange)" + str(len(fileChange)))
    print("len(fileList):"+str(len(fileList)))
    print("len(set(fileList)):"+str(len(list(set(fileList)))))


#新添加的
def handelSameCommit():
    #commitList里面有重复的,和超过10个.py 文件的commit
    global fileChange
    for (key,value) in fileChange.items():
        value1=value[:]
        for j in value:
            if j.getId() in MoreFileCommit:
                value1.remove(j)
        fileChange[key]=value1

# print("zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz")
# #为了防止commit的重复和删除超过10的commit
# for (key,value) in fileChange.items():
#     commitDic={}
#     value2=value[:]
#     for j in value:
#         #重复的commit
#         if j.getId() in commitDic.keys():
#             print("重复的key:",end=" ")
#             print(key)
#             value2.remove(j)
#         else:
#             commitDic[j.getId()]=0
#             #超过10 的commit
#         if j.getId() in MoreFileCommit:
#             value2.remove(j)
#             # print("超过10个commit:",end=" ")
#             # print(j)
#         else:
#             pass
#     fileChange[key]=value2








# with open(r'E:\影响分析\影响分析new\deluge能用2\deluge\fileChange5(Distance4-12-3).csv','w',newline='') as f:
#     csv_write= csv.writer(f)
#     csv_head = ["file1","commit"]
#     csv_write.writerow(csv_head)
#     for (key,value) in fileChange.items():
#         for j in value:
#             csv_write.writerow((key,j.getId()))
# f.close()








def relatedChanges1(commitList_1,commitList_2):
    global CommitDistance,TimeDistance
    count=0
    commmitPairList=[]
    commitList1_tmp={}
    commitList2_tmp={}
    for i in commitList_1:
        commitList1_tmp[i]=0
    for j in commitList_2:
        commitList2_tmp[j]=0
    
    for i in commitList1_tmp.keys():
        for j in commitList2_tmp.keys():
            # print(i.getTime())
            time_1 = datetime.strptime(i.getTime(), "%Y-%m-%d %H:%M:%S")
            time_2 = datetime.strptime(j.getTime(), "%Y-%m-%d %H:%M:%S")
            total_seconds = (time_1 - time_2).total_seconds()
          
            total_hours = (abs(total_seconds))/3600
            if (abs(int(j.getIndex())-int(i.getIndex()))-1) <= CommitDistance and abs(total_hours)<= TimeDistance:               
                count +=1
                commmitPairList.append(commitPair(i,j))       
    return count  






def isUnique(commmitPairList,i,j):
    if len(commmitPairList)==0:
        return True
    else:
        for m in commmitPairList:
            if m.equals(commitPair(i,j)):
                return False
        return True    





def findCoChanges():
    filenum =1
    global fileList
    fileList=list(set(fileList))
    zxynum=0
    fileDic={}
    for i in fileList:
        print(zxynum)
        for j in fileList[filenum:]:
            commitList_1 = fileChange[i]
            commitList_2 = fileChange[j]
            if(len(commitList_1) * len(commitList_2))>=support:
                count=relatedChanges1(commitList_1,commitList_2)
                if count>support:
                    conf1=count/(len(commitList_1))
                    conf2=count/(len(commitList_2))
                    if conf1 >confidence:
                        cochanges.append(filePair(i,j,conf1)) 
                    if conf2>confidence:
                        cochanges.append(filePair(j,i,conf2)) 
                else:
                    pass
        filenum=filenum+1
        zxynum=zxynum+1






def GetCochange(filePath,Threshold1,Threshold2,Threshold3,Threshold4):
    global support,confidence,cochanges,fileChange,fileList,CommitDistance,TimeDistance,MoreFileCommit
    support=Threshold1
    confidence=Threshold2
    CommitDistance=Threshold3
    TimeDistance=Threshold4

    
    cochanges=[]
    fileChange={}
    fileList=[]
    MoreFileCommit=[]

    length=len('historyHandled.txt')
    fileDir=filePath[:-length]  
    filePath1= fileDir+'fileChange51(Distance-%d-%.1f-%d-%d).csv' %(support,confidence,CommitDistance,TimeDistance)
    filePath2= fileDir+'Distance(%d-%.1f-%d-%d).csv' %(support,confidence,CommitDistance,TimeDistance)

    GetMoreFileList(filePath)
    handleHistory(filePath)  
    handelSameCommit()
    findCoChanges()

    with open(filePath1,'w',newline='') as f:
        csv_write= csv.writer(f)
        csv_head = ["file1","commit"]
        csv_write.writerow(csv_head)
        for (key,value) in fileChange.items():
            for j in value:
                csv_write.writerow((key,j))
    f.close()

    with open(filePath2,'w',newline='') as f:
            csv_write= csv.writer(f)
            csv_head = ["file1","file2","count"]
            csv_write.writerow(csv_head)
            for i in cochanges:
                csv_write.writerow((i.getFile1(),i.getFile2(),i.getCount()))

    f.close()
    return filePath2
                
# GetCochange('D:\影响分析\gajim\historyHandled.txt',3,0.2,4,12)
