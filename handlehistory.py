
#加上了删除的行，去除了阈值限制
import re
import os

def first_handle(filePath):
    lineList = []
    # matchPattern = re.compile(r'(^commit)|(^M)|(^R)|(^A)java')
    matchPattern = re.compile(r'(^commit)|(^M)|(^R)|(^A)|(^D)')
    matchPattern2 = re.compile(r'(^commit)')
    matchPattern3 = re.compile(r'(^M)|(^R)|(^A)|(^D)')
    matchPattern4 = re.compile('(.py$)')
    # matchPattern4 = re.compile(r'(.java$)|(.java_$)')
    matchPattern5 = re.compile(r'(^D)')
    file = open(filePath,'r',encoding='UTF-8')  
    
    firstLineflag=True  #判断是否是第一行  
    beforeline= 1 #判断前一行是不是commit
    beforeLine=""  #存储前一行
    i=0
    while 1:
        line = file.readline()
        if not line:
            print("Read file End or Error")
            break
        elif firstLineflag==True and matchPattern2.search(line):    #如果是第一行且是commit行
            beforeLine=line
            beforeline=1     
            firstLineflag=False
        elif firstLineflag==False and matchPattern.search(line):     #如果不是第一行
            if matchPattern2.search(line):   #如果当前行是commit行
                if  beforeline==0 :          #当前行是commit行，前一行不是commit行,添加前一行  
                    lineList.append(beforeLine)
                    beforeLine = line   
                elif beforeline==1 :                       #当前行是commit行，前一行是commit行
                    # print("不做处理")  
                    beforeLine = line                          
                beforeline=1   
                i=i+1                                     #判断是第几个commit    

            elif matchPattern4.search(line) and beforeline==1:                            #如果当前行不是commit行,前一行是commit行，添加前一行和index     
                lineList.append(beforeLine)   
                lineList.append(str(i)+'\n')  
                beforeline=0                 
                beforeLine = line        
            elif matchPattern4.search(line) and beforeline==0:   #如果如果当前行不是commit行,前一行不是commit行，添加前一行                     
                lineList.append(beforeLine)   
                beforeline=0
                beforeLine = line    
            else:
                pass  
        # elif  matchPattern5.search(line) and matchPattern4.search(line):  
        #     print(line)
        else:
            pass
    file.close()
    if matchPattern3.search(beforeLine) and matchPattern4.search(beforeLine):   #如果最后一行是不是commit行，就添加到lineList
        lineList.append(beforeLine) 
    filePath1=os.path.dirname(filePath)+r'\HistoryHandled.txt'
    file = open(filePath1, 'w',encoding='UTF-8')
    for i in lineList:
        file.write(i)
    file.close()
    print(filePath1)
    return filePath1

 
 