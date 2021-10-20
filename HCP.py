from os import path, pipe
import re
import csv 
from collections import namedtuple
from datetime import datetime
import itertools
import collections
from typing import Mapping
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



class MyQUEUE: # just an implementation of a queue

    def __init__(self):
        self.holder = []

    def enqueue(self,val):
        self.holder.append(val)

    def dequeue(self):
        val = None
        try:
            val = self.holder[0]
            if len(self.holder) == 1:
                self.holder = []
            else:
                self.holder = self.holder[1:]   
        except:
            pass
        return val  

    def IsEmpty(self):
        result = False
        if len(self.holder) == 0:
            result = True
        return result
    def prQueue(self):
        print(self.holder)
#设置阈值

Threshold=0
Threshold2=0.0
cochanges=[]
MoreFileCommit=[]
fileChange={}
fileList=[]

defaultFile={}

#计算commit中的文件个数，只包括

def GetMoreFileList(filePath):

    global MoreFileCommit
    matchPattern11 = re.compile(r'(^commit)')
    matchPattern21 = re.compile(r'(^M)|(^A)|(^R)|(^D)')
    file = open(filePath,'r',encoding='UTF-8')


    beforeCommit=''
    fileOneCimmit=0
    for line in file.readlines():
        if matchPattern11.search(line):   #如果commit和time行
            if fileOneCimmit >10:
                MoreFileCommit.append(beforeCommit)
            tmp = line.strip('\n').split(' ',2)[1]
            id = tmp.split('(',2)[0]
            beforeCommit=id
            fileOneCimmit=0
        if matchPattern21.search(line):   #如果时文件信息行M 或A
            fileOneCimmit=fileOneCimmit+1
    #最后一个commit
    if fileOneCimmit>10:
        MoreFileCommit.append(beforeCommit)
    file.close()
    print("len(moreFileCommit):"+str(len(MoreFileCommit)))

def handleHistory(filePath):
    global fileChange,fileList
    DelFileNum=0
    matchPattern1 = re.compile(r'(^commit)')
    matchPattern2 = re.compile(r'(^M)|(^A)')
    matchPattern3 = re.compile(r'(^R)')
    matchPattern4 = re.compile(r'(^\d)')
    matchPattern5 = re.compile(r'(^A)')
    # matchPattern6 = re.compile(r'(_$)')
    matchPattern7 = re.compile(r'(^D)')

    file = open(filePath,'r',encoding='UTF-8')
    


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
            index = line.strip('\n')
        if matchPattern2.search(line):   #如果时文件信息行M 或A
            # commit= commitModel(id,time,index)
            # fileName = line.strip('\n').split('	',2)[1]
            fileName = line.strip('\n').split('	',1)[1]
            # print("fileName:"+fileName)
            if fileName in fileChange.keys():
                commitList=[]
                commitList = fileChange[fileName]
                print(len(commitList),end="  ")
                commitList.append(id)
                print(len(commitList))
                print("---------------------------------------------")
                fileChange[fileName] = commitList
            else:
                commitList = []
                commitList.append(id)
                fileChange[fileName] = commitList
                fileList.append(fileName)
        if matchPattern3.search(line):   #如果时文件信息行R
            # commit= commitModel(id,time,index)
            # fileName = line.strip('\n').split()[1]
            # fileNewName = line.strip('\n').split()[2]
            fileNewName = line.strip('\n').split('	',2)[2]
            fileName = line.strip('\n').split('	',2)[1]
            
            if fileName in fileChange.keys():      #没有考虑fileNewName也在commitList中的情况   fileNewName本来就存在，其他的又重命名为了 fileNewName
                # print("执行了")
                commitList = []
                commitList = fileChange.pop(fileName)
                commitList.append(id)
                
                if fileNewName in fileChange.keys():              
                    fileChange[fileNewName]=commitList+fileChange[fileNewName]
                    fileList.remove(fileName)
                else:
                    fileChange[fileNewName]=commitList
                    fileList.remove(fileName)
                    fileList.append(fileNewName)

            else:
                # print(fileName)
                commitList = []
                commitList.append(id)
                if fileNewName in fileChange.keys():
                    fileChange[fileNewName]=commitList+fileChange[fileNewName]
                else:
                    fileChange[fileNewName]=commitList
                    fileList.append(fileNewName)

        if matchPattern7.search(line):
            DelFileNum=DelFileNum+1
            # fileName = line.strip('\n').split('	',2)[1]
            fileName = line.strip('\n').split('	',1)[1]
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
    print("==================================")

    print("del file:"+str(DelFileNum))
    print("len(fileChange)" + str(len(fileChange)))
    print("len(fileList):"+str(len(fileList)))
    print("len(set(fileList)):"+str(len(list(set(fileList)))))



def handelSameCommit():
    #commitList里面有重复的,和超过10个.py 文件的commit
    for (key,value) in fileChange.items():
        value=list(set(value)-set(MoreFileCommit))
        value=list(set(value))
        fileChange[key]=value




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
    global defaultFile
    # print(type(itertools.groupby(fileList)))
    # fileList1=list(itertools.groupby(fileList))
    fileList1=list(set(fileList))
    print(len(fileList1))
    zxynum=0
    fileDic={}
    for i in fileList1:
        
        # print(i+"  "+str(len(fileChange[i])))
        # print(zxynum)
        
        commitList_1 = fileChange[i]
        for j in fileList1[filenum:]:
            
           
            # count=0
            commitList_2 = fileChange[j]
            commitCommmenList=[]
            commitCommmenList=[zzz for zzz in commitList_1 if zzz in commitList_2]
            # for oneC in commitList_1:
            #     if oneC in commitList_2:
            #         commitCommmenList.append(oneC)
            #         count+=1
            # print(len(commitCommmenList))
            if len(commitList_1)==0 or len(commitList_2)==0:
                if len(commitList_1)==0:
                    defaultFile.setdefault(i,[])
                    print(i)
                elif len(commitList_2)==0:
                    defaultFile.setdefault(j,[])
                    print(j)                   
            
            else:
                conf1=len(commitCommmenList)/(len(commitList_1))
                conf2=len(commitCommmenList)/(len(commitList_2))
                if len(commitCommmenList)>Threshold and conf1>Threshold2 :
                    cochanges.append(filePair(i,j,conf1))
                if len(commitCommmenList)>Threshold and conf2>Threshold2 :
                    cochanges.append(filePair(j,i,conf2))                
        filenum=filenum+1
        zxynum=zxynum+1
# def findCoChanges():
#     filenum =1
#     for i in range(len(fileList)-1):
#         for j in range(i+1,len(fileList)):
#             commitList_1 = fileChange[fileList[i]]
#             commitList_2 = fileChange[fileList[j]]
#             if(len(commitList_1) * len(commitList_2))>=Threshold:
#                 count=relatedChanges1(commitList_1,commitList_2)
#                 if count>=Threshold:
#                     cochanges.append(filePair(fileList[i],fileList[j],str(count))) 
#         filenum = filenum+1


AllFiles={}
FileNum=[]
FileMatrix={}
FileMatrixHCP={}



def BFS(graph,start,end,q):
    # print("执行了",start,end)
    FinalResult=[]
    temp_path = [start]
    q.enqueue(temp_path)
    # print('start',start,'end',end)
    while q.IsEmpty() == False:
        tmp_path = q.dequeue()
        last_node = tmp_path[len(tmp_path)-1]
        # print('last_node',last_node)
        if last_node == end:
            # print("VALID_PATH : ",tmp_path)
            FinalResult.append(tmp_path)
        # print(AllFiles[last_node])
        for link_node in graph[last_node]:
            if link_node not in tmp_path:
                new_path = []
                new_path = tmp_path + [link_node]
                q.enqueue(new_path)
    return FinalResult


def getMAXConf(PathList):
    MaxConf=0
    for onePath in PathList:
        conf=1
        for num in range(0,(len(onePath)-1)):
            conf = conf * FileMatrix[onePath[num],onePath[num+1]]
        if conf > MaxConf:
            MaxConf=conf
    return MaxConf      
                        

def GetCochange(filePath,support,confidence):
    global Threshold,Threshold2,cochanges,fileChange,fileList,AllFiles,FileMatrix,FileMatrixHCP
    FileMatrix= collections.defaultdict(lambda:0)
    FileMatrixHCP=collections.defaultdict(lambda:0)
    Threshold=support
    Threshold2=confidence

    length=len('historyHandled.txt')
    fileDir=filePath[:-length]
    filePath1= fileDir+'fileChange51(HCP-%d-%.1f).csv' %(Threshold,Threshold2)
    filePath2= fileDir+'HCP(%d-%.1f).csv' %(Threshold,Threshold2)

    GetMoreFileList(filePath)
    handleHistory(filePath)  
    handelSameCommit()
    findCoChanges()
    print("len(cochange)"+str(len(cochanges)))
    with open(filePath1,'w',newline='') as f:
        csv_write= csv.writer(f)
        csv_head = ["file1","commit"]
        csv_write.writerow(csv_head)
        for (key,value) in fileChange.items():
            for j in value:
                csv_write.writerow((key,j))
    f.close()


    for i in cochanges:
        file1=i.getFile1()
        file2=i.getFile2()
        file1Num=0
        file2Num=0

        if file1 in FileNum:
            pass
        else:
            FileNum.append(file1)
        file1Num=FileNum.index(file1)
        
        if file2 in FileNum:
            pass
        else:
            FileNum.append(file2)
        file2Num=FileNum.index(file2)

        if file1Num in AllFiles.keys():
            AllFiles[file1Num].append(file2Num)
        else:
            AllFiles[file1Num]=[file2Num]
        
        if file2Num in AllFiles.keys():
            pass
        else:
            AllFiles[file2Num]=[]

        FileMatrix[file1Num,file2Num]=i.getCount()


    print(len(FileNum)) 
    print(FileMatrix)
    # for i in range(0,len(FileNum)):
    #     for j in range(0,len(FileNum)):
    #         if FileMatrix[i,j]==0:
    #             print(i,j)


    for i in range(0,len(FileNum)):
        for j in range(0,len(FileNum)):
            if i==j:
                pass
            elif FileMatrix[i,j]==0: 
                path_queue = MyQUEUE()
                # path_queue.prQueue()
                finalResult= BFS(AllFiles,i,j,path_queue)
                # print('len(FinalResult)',len(finalResult))
                MAXConf=getMAXConf(finalResult)
                FileMatrix[i,j]=MAXConf
                # FileMatrixHCP[i,j]=MAXConf
                # print(MAXConf)
            else:
                pass
    print("-------------------------------------")
  
    with open(filePath2,'w',newline='') as f:
        csv_write= csv.writer(f)
        csv_head = ["file1","file2","count"]
        csv_write.writerow(csv_head)
        for i in range(0,len(FileNum)):
            for j in range(0,len(FileNum)):
                if i==j:
                    pass
                # elif FileMatrixHCP[i,j]==0:
                elif FileMatrix[i,j]==0:
                    pass
                else:
                    # csv_write.writerow((FileNum[i],FileNum[j],FileMatrixHCP[i,j]))
                    csv_write.writerow((FileNum[i],FileNum[j],FileMatrix[i,j]))
    f.close()
    return filePath2
                
# GetCochange('D:\影响分析\gajim\historyHandled.txt',3,0.2)
