

import matplotlib.pyplot as plt
import re
def doonfile():

    data = open("data/data3/00.log",'r')
    lines = data.readlines()
    newdata = open("data/data3/0.log",'w')
    for line in lines:
        if line.find("send") >= 0 or line.find("retreat")>=0:
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
    ratelist = getRate(lines,droplist)
    data.close()
    return ratelist, meantimelist, fairlist
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
    print droplist
    ratelist = list()
    i = 0
    for line in lines:
        if line.find("req") >= 0:
            tup = re.search('\d+\staken:\s\d+',line).span()
            line = line[tup[0]:tup[1]]
            reqtaken = line.split(" taken: ")
            ratelist.append((float(reqtaken[1])-droplist[i])/float(reqtaken[0]))
            i+=1

    return ratelist
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



    # xplot =list()
    # for i in range(len(ti'melist)):
    #     xplot.append(1)
    # print len(xplot)
    # print len(timelist)
    # plt.scatter(xplot,timelist, s=0.01)
    # plt.show()





if __name__ == '__main__':
    # doonfile()
    r0,m0,f0= draw("data/data3/0.log")
    r1,m1,f1=draw("data/data3/1.log")
    r2,m2,f2=draw("data/data3/2.log")
    file =open("data/data3/plotdata.log",'w')
    for t in r0:
        file.write(str(t))
        file.write(' ')
    file.write('\n')
    for t in r1:
        file.write(str(t))
        file.write(' ')
    file.write('\n')
    for t in r2:
        file.write(str(t))
        file.write(' ')
    file.write('\n')

    for t in m0:
        file.write(str(t))
        file.write(' ')
    file.write('\n')
    for t in m1:
        file.write(str(t))
        file.write(' ')
    file.write('\n')
    for t in m2:
        file.write(str(t))
        file.write(' ')
    file.write('\n')

    for t in f0:
        file.write(str(t))
        file.write(' ')
    file.write('\n')
    for t in f1:
        file.write(str(t))
        file.write(' ')
    file.write('\n')
    for t in f2:
        file.write(str(t))
        file.write(' ')
    file.write('\n')
    file.close()




