

import matplotlib.pyplot as plt
import re
def doonfile():

    data = open("data/data4/22.log",'r')
    newdata = open("data/data4/2.log",'w')
    lines = data.readlines()
    for line in lines:
        if line.find("send") >= 0 or line.find("retreat")>=0 or line.find("time")>=0:
            continue
        else:
            line = line.replace(" - ["," ")
            line = line.replace("] - "," ")
            newdata.write(line)
    data.close()
    newdata.close()

def draw(path):


    meantimelist = list()
    fairlist = list()
    data =  open(path,'r')
    lines = data.readlines()
    droplist = list()

    head = len(lines)-1
    for i in range(len(lines)-1, -1,-1):
        if lines[i].find("True") >=0 or lines[i].find("False")>=0:
            tail = head
            head = i
            time,dropnum = getMeanTime(path, lines, head, tail)

            meantimelist.insert(0,time)
            droplist.insert(0,dropnum)
            fairness = getFairness(path, lines,head,tail)
            fairlist.insert(0,fairness)
    ratelist, reqtakennum = getRate(lines,droplist)
    data.close()
    print 'success rate',ratelist
    print 'mean time' ,meantimelist
    print 'fair list', fairlist
    print 'taken num', reqtakennum
    return ratelist, meantimelist, fairlist,reqtakennum
def getMeanTime(path, lines, head, tail):
    drop = 0
    sum = 0
    num = 0
    for i in range(head,tail):
        line = lines[i]
        start = line.find("[")
        end = line.find("]")
        if start < 0:
            continue
        str = line[start+1:end].replace(" ","")
        str = str.split(",")
        for time in str:
            if len(time)==0:
                continue
            if float(time) <25:
                num  +=1
                sum = sum+float(time)
            else:
                drop+=1
    if num == 0:
        return 0,drop
    else:
        return sum/num,drop


def getRate(lines,droplist):
    # print droplist
    ratelist = list()
    reqtakenlist = list()
    i = 0
    for line in lines:
        if line.find("req") >= 0:
            tup = re.search('\d+\staken:\s\d+',line).span()
            line = line[tup[0]:tup[1]]
            reqtaken = line.split(" taken: ")
            ratelist.append((float(reqtaken[1])-droplist[i])/float(reqtaken[0]))
            reqtakenlist.append((float(reqtaken[1])-droplist[i]))
            # print reqtaken
            i+=1

    return ratelist,reqtakenlist
def getFairness(path, lines, head, tail):
    reqsum=0
    reqsquaresum=0
    node=0
    for i in range(head,tail):
        line = lines[i]
        start = line.find("[")
        end = line.find("]")
        if start < 0:
            continue
        str = line[start+1:end].replace(" ","")
        str = str.split(",")
        reqsum+=len(str)
        reqsquaresum+=(len(str))*len(str)
        node = node+1
    return reqsum*reqsum*10000/reqsquaresum/node

def writeCleanData(n0, n1,n2):
    file = open("data/data4/plotdata.log", 'a')
    for t in n0:
        file.write(str(t))
        file.write(' ')
    file.write('\n')
    for t in n1:
        file.write(str(t))
        file.write(' ')
    file.write('\n')
    for t in n2:
        file.write(str(t))
        file.write(' ')
    file.write('\n')
    file.close()




if __name__ == '__main__':
    # doonfile()

    #
    r0,m0,f0,t0= draw("data/data4/0.log")
    r1,m1,f1,t1=draw("data/data4/1.log")
    r2,m2,f2,t2=draw("data/data4/2.log")

    writeCleanData(r0,r1,r2)
    writeCleanData(m0, m1, m2)
    writeCleanData(f0, f1, f2)
    writeCleanData(t0, t1, t2)






