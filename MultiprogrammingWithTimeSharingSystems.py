import time
import random
import copy

a=1
elapsed=0
thirty = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30]
no_resources = random.randint(1,30)
no_users = random.randint(1,30)

rList = []
uList = []
queue = []
Q = []
waitList = []
resourceList = []
resourceList2 = []
resourceList3 = []
timeList = []
timeList2 = []
finishedList = []
finishedList2 = []
compRList = []
compRList2 = []
waitingTime = []
noList = []
ruList = []
orR = []
orU = []
orQ = []
origQ = []
origT = []
orT = []
orW = []

def getResource(elem):
    return elem[1]

def getUser(elem):
    return elem[0]

def UserCount(li, elem):
    a=0
    for i in range(len(li)):
        if li[i] == elem:
            a+=1
    return a

def searchDuplicates(li, e1, e2):
    for i in range(len(li)):
        if li[i][0] == e1 and li[i][1] == e2:
            return True
    else:
        return False

r = random.sample(thirty, no_resources)
u = random.sample(thirty, no_users)

print("Generated users: ", u)
print("Generated resources: ", r)

orU=copy.deepcopy(u)
orR=copy.deepcopy(r)

r.sort()
u.sort()

for i in range(len(u)):
    ranR = random.randint(0,len(r)-1)
    ranU = random.randint(0,len(u)-1)
    ranT = random.randint(1,30)
    while searchDuplicates(queue, u[ranU], r[ranR]):
        ranR = random.randint(0,len(r)-1)
        ranU = random.randint(0,len(u)-1)
        ranT = random.randint(1,30)
    data = [u[ranU], r[ranR], ranT]
    queue.append(data)
    resourceList2.append(r[ranR])

for i in range(len(r)):
    data = [r[i], 0]
    compRList.append(data)

for i in range(len(compRList)):
    cResource = compRList[i][0]
    for j in range(30):
        if j+1 == cResource:
            uc = UserCount(resourceList2, j+1)
            compRList[i][1] = uc

queue.sort()
compRList2 = copy.deepcopy(compRList)

print()
for i in range(len(queue)):
    print("User", queue[i][0], "is requesting Resource", queue[i][1], "for", queue[i][2], "seconds")
    origQ.append(queue[i])
    origT.append(queue[i][2])

for i in range(0,len(queue)-1):
    try:
        j=i+1
        while j<len(queue):
            if (queue[i][0] == queue[j][0]):
                waitList.append(queue.pop(j))
                j=i
            else:
                if (queue[i][1] == queue[j][1]):
                    waitList.append(queue.pop(j))
                    j=i
                
            j+=1     
    except:
        pass
    
orQ = copy.deepcopy(queue)
orW = copy.deepcopy(waitList)

for i in range(len(queue)):
    timeList.append(queue[i][2])
    resourceList.append(queue[i][1])
    
timeList2 = copy.deepcopy(timeList)
resourceList3 = copy.deepcopy(resourceList)

print()

def printStatus():

    print(".....QUEUE.....")
    print()
    i = 0
    while i<(len(queue)):
        cUser = queue[i][0]
        cResource = queue[i][1]
        cTime = queue[i][2]
        if queue[i][2] > 0:
            totalTime = cTime
            waitingU = compRList[r.index(cResource)][1]-1
            for j in range(len(waitList)):
                if waitList[j][1] == cResource:
                    totalTime = totalTime + waitList[j][2]
            print("User#", cUser, "is using Resource#", cResource, " [[Time remaining:", cTime, "]]  *Users in wait:", waitingU, "* [[Time until user-free: ", totalTime,"]]")
            
                
        else:
            busy = False
            for j in range(len(waitList)):
                if queue[i][1] == waitList[j][1]:
                    for p in range(len(queue)):
                        if waitList[j][0] == queue[p][0]:
                            busy = True
                            break
                    if busy:
                        continue
                    if (compRList[r.index(cResource)][1]-1)>=1:
                        if queue[i] not in finishedList:
                            compRList[r.index(cResource)][1]=compRList[r.index(cResource)][1]-1 
                            finishedList.append(queue[i])
                        queue[i]=waitList[j]
                        timeList[i]=(waitList[j][2])
                        waitList.remove(waitList[j])
                        cUser = queue[i][0]
                        cResource = queue[i][1]
                        cTime = queue[i][2]
                        totalTime = cTime
                        waitingU = compRList[r.index(cResource)][1]-1
                        for j in range(len(waitList)):
                            if waitList[j][1] == cResource:
                                totalTime = totalTime + waitList[j][2]
                        print("User#", cUser, "is now using Resource#", cResource, " [[Time remaining:", cTime, "]]  *Users in wait:", waitingU, "* [[Time until user-free: ", totalTime,"]]")
                        
                        break
                    else:
                        compRList[r.index(cResource)][1]=compRList[r.index(cResource)][1]-1 
                        finishedList.append(queue[i])
                        queue.pop(i)
                        timeList.pop(i)
                        i-=1
                        if i<0:
                            i=-1
                        break
                
            else:
                if len(waitList)>=1:
                    for k in range(len(waitList)):
                        if waitList[k][0] == queue[i][0]:
                            queue[i] = waitList[k]
                    else:
                        compRList[r.index(cResource)][1]=compRList[r.index(cResource)][1]-1 
                        finishedList.append(queue[i])
                        queue.pop(i)
                        timeList.pop(i)
                        i-=1
                        if i<0:
                            i=-1
                else:
                        compRList[r.index(cResource)][1]=compRList[r.index(cResource)][1]-1 
                        finishedList.append(queue[i])
                        queue.pop(i)
                        timeList.pop(i)
                        i-=1
                        if i<0:
                            i=-1

        i+=1
    
    for i in range(len(compRList)):
        if compRList[i][1]==0:
            print("Resource#", compRList[i][0], "is free")
        else:
            for j in range(len(waitList)):
                if compRList[i][0] == waitList[j][1]:
                    for k in range(len(queue)):
                        if compRList[i][0] == queue[k][1]:
                            break
                    else:
                        print("Resource#", compRList[i][0], "has been requested")
                    

    
    print()
    print(".....WAITING.....")
    print()
    
    w=0
    while w < len(waitList):
        cUser = waitList[w][0]
        cResource = waitList[w][1]
        cTime = waitList[w][2]
        y=0
        for x in range(len(queue)):
            if cResource == queue[x][1]:
                y = queue[x][2]
                for z in range(len(queue)):
                    if cUser == queue[z][0]:
                        if y < queue[z][2]:
                            y = queue[z][2]
                        break
                else:
                    y = queue[x][2]
                    break
        else:
            for x in range(len(queue)):
                if cUser == queue[x][0]:
                    y = queue[x][2]
                    break
        waitTime = y
        
        for j in range(0, w):
            if waitList[j][1] == waitList[w][1]:
                waitTime = waitTime + waitList[j][2]
        
        if waitTime == 0:
            timeList.append(waitList[w][2])
            queue.append(waitList.pop(w))
            w-=1
        else:
            print("User#", cUser, "is waiting to use Resource#", cResource, "[[Time till usage:", waitTime,"]]")
        w+=1

    print()
    print(".....FINISHED.....")
    print()

    for i in range(len(finishedList)):
        cUser = finishedList[i][0]
        cResource = finishedList[i][1]
        print("User#", cUser, "has finished with Resource#", cResource)
    print()
    
    
def initialSnapshot():
    print("\n==Original Snapshot==\n")
    print(".....QUEUE.....")
    print()
    i = 0
    while i<(len(orQ)):
        cUser = orQ[i][0]
        cResource = orQ[i][1]
        cTime = orQ[i][2]
        if orQ[i][2] > 0:
            totalTime = cTime
            waitingU = compRList2[r.index(cResource)][1]-1
            for j in range(len(orW)):
                if orW[j][1] == cResource:
                    totalTime = totalTime + orW[j][2]
            print("User#", cUser, "is using Resource#", cResource, " [[Time remaining:", cTime, "]]  *Users in wait:", waitingU, "* [[Time until user-free: ", totalTime,"]]")
        else:
            busy = False
            for j in range(len(orW)):
                if orQ[i][1] == orW[j][1]:
                    for p in range(len(orQ)):
                        if orW[j][0] == orQ[p][0]:
                            busy = True
                            break
                    if busy:
                        continue
                    if (compRList2[r.index(cResource)][1]-1)>=1:
                        if orQ[i] not in finishedList2:
                            compRList2[r.index(cResource)][1]=compRList2[r.index(cResource)][1]-1 
                            finishedList2.append(orQ[i])
                        orQ[i]=orW[j]
                        timeList2[i]=(orW[j][2])
                        orW.remove(orW[j])
                        cUser = orQ[i][0]
                        cResource = orQ[i][1]
                        cTime = orQ[i][2]
                        totalTime = cTime
                        waitingU = compRList2[r.index(cResource)][1]-1
                        for j in range(len(orW)):
                            if orW[j][1] == cResource:
                                totalTime = totalTime + orW[j][2]
                        print("User#", cUser, "is now using Resource#", cResource, " [[Time remaining:", cTime, "]]  *Users in wait:", waitingU, "* [[Time until user-free: ", totalTime,"]]")
                        break
                    else:
                        compRList2[r.index(cResource)][1]=compRList2[r.index(cResource)][1]-1 
                        finishedList2.append(orQ[i])
                        orQ.pop(i)
                        timeList2.pop(i)
                        i-=1
                        if i<0:
                            i=-1
                        break
                
            else:
                if len(orW)>=1:
                    for k in range(len(orW)):
                        if orW[k][0] == orQ[i][0]:
                            orQ[i] = orW[k]
                    else:
                        compRList2[r.index(cResource)][1]=compRList2[r.index(cResource)][1]-1 
                        finishedList2.append(orQ[i])
                        orQ.pop(i)
                        timeList2.pop(i)
                        i-=1
                        if i<0:
                            i=-1
                else:
                        compRList2[r.index(cResource)][1]=compRList2[r.index(cResource)][1]-1 
                        finishedList2.append(orQ[i])
                        orQ.pop(i)
                        timeList2.pop(i)
                        i-=1
                        if i<0:
                            i=-1

        i+=1
    
    for i in range(len(compRList2)):
        if compRList2[i][1]==0:
            print("Resource#", compRList2[i][0], "is free")
        else:
            for j in range(len(orW)):
                if compRList2[i][0] == orW[j][1]:
                    for k in range(len(orQ)):
                        if compRList2[i][0] == orQ[k][1]:
                            break
                    else:
                        print("Resource#", compRList2[i][0], "has been requested")

    
    print()
    print(".....WAITING.....")
    print()
    
    w=0
    while w < len(orW):
        cUser = orW[w][0]
        cResource = orW[w][1]
        cTime = orW[w][2]
        y=0
        for x in range(len(orQ)):
            if cResource == orQ[x][1]:
                y = orQ[x][2]
                for z in range(len(orQ)):
                    if cUser == orQ[z][0]:
                        if y < orQ[z][2]:
                            y = orQ[z][2]
                        break
                else:
                    y = orQ[x][2]
                    break
        else:
            for x in range(len(orQ)):
                if cUser == orQ[x][0]:
                    y = orQ[x][2]
                    break
        waitTime = y
        
        for j in range(0, w):
            if orW[j][1] == orW[w][1]:
                waitTime = waitTime + orW[j][2]
        
        if waitTime == 0:
            timeList2.append(orW[w][2])
            orQ.append(orW.pop(w))
            w-=1
        else:
            print("User#", cUser, "is waiting to use Resource#", cResource, "[[Time till usage:", waitTime,"]]")
        w+=1

    print()

def updateStatus():
    for i in range(len(queue)):
        if queue[i][2] == 0:
            continue
        y = queue[i][2] - 1
        queue[i][2] = y
    for i in range(len(queue)):
        if len(timeList)==0:
            timeList.append(queue[i][2])
        else:
            timeList[i] = queue[i][2]

def checker(): 
    
    if len(queue)==0 and len(waitList)==0:
        return False
    else:
        result = timeList.count(timeList[0]) == len(timeList)
        if result and timeList[0]==0 and len(waitList)==0:
            return False
        else:
            return True

print()
print("==================================================")

#while a:
initialSnapshot()
print()
print("==================================================")
print()

#print("Generated users:    ", orU, "\nGenerated resources:", orR,"\n")

#for i in range(len(origQ)):
#    print("User", origQ[i][0], "requested Resource", origQ[i][1], "for", origT[i], "seconds")
#print()



