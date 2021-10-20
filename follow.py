
import os
from git.repo import Repo
from git import Git
import csv

Threshold=0
Threshold2=0.0
commonList=[]
def all_path(dirname):
    filter=[".py"]
    result1 = []#所有的文件  完整的路径
    result2=[]             #文件在项目中的路径
    dirlen = len(dirname)
    zxy=0
    for maindir, subdir, file_name_list in os.walk(dirname):
        for filename in file_name_list:
            apath = os.path.join(maindir, filename)#合并成一个完整路径
            ext = os.path.splitext(apath)[1] # 将'ab.py' 分为('ab', 'py')
            apath1= apath[dirlen+1:]
            if ext in filter:
                result1.append(apath)  
                result2.append(apath1)    
            zxy=zxy+1                  
    return result2



def GetCochange(fileDir,support,confidence):
    global Threshold,Threshold2,commonList
    commonList=[]
    Threshold=support
    Threshold2=confidence

    R=Git(fileDir)
    AllFile=all_path(fileDir)
    AllFile=[i.replace('\\','/') for i in AllFile]
    fileDic={}
    Already=0
    for i in AllFile:
        Already=Already+1
        print(Already)
        ExecuteSent="git log --no-merges --pretty='%%H' -M100%% --follow  %s" %i
        fileDic[i]=R.execute(ExecuteSent)  
        fileDic[i] = fileDic[i].replace('\'','').split('\n')

    FileList=list(fileDic.keys())
    fileNum=1
    for i in FileList:
        CommitIdListOne=fileDic[i]
        for j in FileList[fileNum:]:
            CommitIdListTwo=fileDic[j]
            CommitCommmenList=[zzz for zzz in CommitIdListOne if zzz in CommitIdListTwo]
            if len(CommitCommmenList)>Threshold:
                conf1=len(CommitCommmenList)/len(CommitIdListOne)
                conf2=len(CommitCommmenList)/len(CommitIdListTwo)
                if conf1>Threshold2:
                    commonList.append((i,j,conf1))
                if conf2>Threshold2:
                    commonList.append((j,i,conf2))
            else:
                pass
        fileNum=fileNum+1  
    
    filePath=fileDir+r'\follow(%d-%.1f).csv' %(Threshold,Threshold2)
    with open(filePath,'w',newline='') as f:
            csv_write= csv.writer(f)
            csv_head = ["file1","file2","count"]
            csv_write.writerow(csv_head)
            for cc in commonList:
                csv_write.writerow((cc[0],cc[1],cc[2]))

    f.close()
    return filePath
