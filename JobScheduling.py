import copy

def readFile(fileDirectory):
    entry = {'Process':1, 'Arrival':1, 'Burst Time':1, 'Priority':1}
    process = []
    processList = []
    with open(fileDirectory,"r") as f:
        line = f.readline()
        while line != '':
            line = f.readline()
            char = ""
            
            for i in range(0, len(line)):
                if(line[i] == '\t' or line[i] == '\n' or line[i] == ''):
                    continue
                char+=line[i]
                try:
                    if line[i+1] == '\t' or line[i+1] == '\n' or line[i+1] == '':
                        process.append(char)
                        char = ""
                except:
                    process.append(char)
            if process == []:
                break
            entry['Process'] = int(process[0])
            entry['Arrival'] = int(process[1])
            entry['Burst Time'] = int(process[2])
            entry['Priority'] = int(process[3])
            processList.append(entry)
            process = []
            entry = {'Process':0, 'Arrival':0, 'Burst Time':0, 'Priority':0}

    return processList


def getBurstTime(elem):
    return elem['Burst Time']

def getPriority(elem):
    return elem['Priority']

def getArrivalTime(elem):
    return elem['Arrival']

def FCFS(processList):
    print("===================================\nFirst-Come-First-Served Scheduling\n")
    sumW = []
    sumT = []
    for x in range(0,len(processList)):
        sum1 = 0
        sum2 = processList[0]['Burst Time']
        if(x == 0):
            print("Process", processList[x]['Process'],"Waiting Time : 0 , Turnaround Time: ", processList[x]['Burst Time'])
            sumW.append(0)
            sumT.append(processList[x]['Burst Time'])
            continue
        for i in range(x,0,-1):
            sum1 = sum1 + processList[i-1]['Burst Time']
            sum2 = sum2 + processList[i]['Burst Time']
        sumW.append(sum1)
        sumT.append(sum2)
        print("Process", processList[x]['Process'],"Waiting Time :",sum1,", Turnaround Time: ", sum2)
    total1 = 0
    total2 = 0
    for i in sumW:
        total1 = total1 + i
    for i in sumT:
        total2 = total2 + i
    avg1 = round(total1/len(sumW), 2)
    avg2 = round(total2/len(sumT), 2)
    print("\nAverage Waiting Time: ", avg1, " Average Turnaround Time: ", avg2)
    print()

def SJF(processList):
    print("===================================\nShortest Job First Scheduling\n")
    sumW = []
    sumT = []
    copy_PL = copy.copy(processList)
    copy_PL.sort(key=getBurstTime)
    for x in range(0, len(copy_PL)):
        sum1 = 0
        sum2 = copy_PL[0]['Burst Time']
        if(x == 0):
            print("Process", copy_PL[x]['Process'],"Waiting Time : 0, Turnaround Time: ", copy_PL[x]['Burst Time'])
            sumW.append(0)
            sumT.append(copy_PL[x]['Burst Time'])
            continue
        for i in range(x,0,-1):
            sum1 = sum1 + copy_PL[i-1]['Burst Time']
            sum2 = sum2 + copy_PL[i]['Burst Time']
        sumW.append(sum1)
        sumT.append(sum2)
        print("Process", copy_PL[x]['Process'],"Waiting Time :",sum1,", Turnaround Time: ", sum2)
    total1 = 0
    total2 = 0
    for i in sumW:
        total1 = total1 + i
    for i in sumT:
        total2 = total2 + i
    avg1 = round(total1/len(sumW), 2)
    avg2 = round(total2/len(sumT), 2)
    print("\nAverage Waiting Time: ", avg1, " Average Turnaround Time: ", avg2)
    print()

def SRPT(processList):
    print("===================================\nShortest Remaining Processing Time Scheduling\n")
    sumW = []
    sumT = []
    
    copy_PL = copy.deepcopy(processList)
    for i in range(0,len(copy_PL)):
        sumW.append(0)
        sumT.append(0)
    copy_PL.sort(key=getArrivalTime)
    curr = 0
    x = 0
    arrivals = []
    timeline = []
    popped = False

    while(True):
        a = list(filter(lambda process: process['Arrival'] == x, copy_PL))
        if a:
            arrivals.extend(a) #append processes according to arrival time
            c = curr
            curr = next((i for i, item in enumerate(arrivals) if item['Burst Time'] < arrivals[c]['Burst Time'] and item['Burst Time'] > 0 and item['Burst Time'] > 0), c)
            if (curr != c or popped):
                if (sumW[arrivals[curr]['Process']] == 0):
                    sumW[arrivals[curr]['Process']-1] = x - arrivals[curr]['Arrival']
                    popped = False
            arrivals[curr]['Burst Time'] = arrivals[curr]['Burst Time'] - 1
            timeline.append(arrivals[curr]['Process'])
            if arrivals[curr]['Burst Time'] == 0:
                sumT[arrivals[curr]['Process']-1] = x + 1
                newcurr = 0
                arrivals.pop(curr)
                for i in range(0,len(arrivals)):
                    if arrivals[i]['Burst Time'] < arrivals[newcurr]['Burst Time']:
                        newcurr = i
                        popped = True
                curr = newcurr
                
        if not arrivals:
            break
        if not a:
            arrivals.sort(key=getBurstTime)
            curr = 0
            p = True
            while(arrivals):
                if p:
                    tmp = arrivals[curr]['Process'] - 1
                    if (sumW[tmp] == 0):
                        sumW[tmp] = x - arrivals[curr]['Arrival'] - (processList[tmp]['Burst Time']-arrivals[curr]['Burst Time'])
                    p = False
                arrivals[curr]['Burst Time'] = arrivals[curr]['Burst Time'] - 1
                timeline.append(str(arrivals[curr]['Process'])+"!")
                if arrivals[curr]['Burst Time'] == 0:
                    tmp = arrivals[curr]['Process'] - 1
                    sumT[tmp] = x + 1
                    arrivals.pop(curr)
                    p = True
                x = x+1
        x = x+1
        
    for x in range(0, len(copy_PL)):
        print("Process", copy_PL[x]['Process'],"Waiting Time :",sumW[x],", Turnaround Time: ", sumT[x])
    total1 = 0
    total2 = 0
    for i in sumW:
        total1 = total1 + i
    for i in sumT:
        total2 = total2 + i
    avg1 = round(total1/len(sumW), 2)
    avg2 = round(total2/len(sumT), 2)
    print("\nAverage Waiting Time: ", avg1, " Average Turnaround Time: ", avg2)
    print()
    

def Priority(processList):
    print("===================================\nPriority Scheduling\n")
    sumW = []
    sumT = []
    copy_PL = copy.copy(processList)
    copy_PL.sort(key=getPriority)
    for x in range(0, len(copy_PL)):
        sum1 = 0
        sum2 = copy_PL[0]['Burst Time']
        if(x == 0):
            print("Process", copy_PL[x]['Process'],"Waiting Time : 0, Turnaround Time: ", copy_PL[x]['Burst Time'])
            sumW.append(0)
            sumT.append(copy_PL[x]['Burst Time'])
            continue
        for i in range(x,0,-1):
            sum1 = sum1 + copy_PL[i-1]['Burst Time']
            sum2 = sum2 + copy_PL[i]['Burst Time']
        sumW.append(sum1)
        sumT.append(sum2)
        print("Process", copy_PL[x]['Process'],"Waiting Time :",sum1,", Turnaround Time: ", sum2)
    total1 = 0
    total2 = 0
    for i in sumW:
        total1 = total1 + i
    for i in sumT:
        total2 = total2 + i
    avg1 = round(total1/len(sumW), 2)
    avg2 = round(total2/len(sumT), 2)
    print("\nAverage Waiting Time: ", avg1, " Average Turnaround Time: ", avg2)
    print()

def checkEmpty(processList):
    for i in range(0,len(processList)):
        if (processList[i]['Burst Time'] != 0):
            return False
    return True

def RoundRobin(processList):
    print("===================================\nRound-Robin Scheduling\n")
    quantum = 4
    sumW = []
    sumT = []
    copy_PL = copy.deepcopy(processList)
    for i in range(0,len(copy_PL)):
        sumW.append(0)
        sumT.append(0)
    cPL = copy.deepcopy(copy_PL)
    curr = 0
    x = 1
    newQ = 0
    mark = -1
    while(not checkEmpty(cPL)):
        cPL[curr]['Burst Time'] = cPL[curr]['Burst Time'] - 1
        mark = curr
        if (cPL[curr]['Burst Time'] == 0):
            if (x-newQ<=quantum):
                sumW[curr] = newQ - (copy_PL[curr]['Burst Time'] - (x-newQ))
            newQ = x
            sumT[curr] = x
            curr = curr+1
            if (curr>(len(cPL)-1)):   
                curr = 0
            mark = curr
            while (cPL[curr]['Burst Time'] == 0):
                curr = curr+1
                if (curr>(len(cPL)-1)):
                    curr = 0
                if curr == mark:
                    break
        elif x==(newQ+quantum) and x>0:
            loopFlag = 0
            sumT[curr] = x
            newQ = x
            curr = curr+1
            if (curr>(len(cPL)-1)):   
                curr = 0
            while (cPL[curr]['Burst Time'] == 0):
                curr = curr+1
                if (curr>(len(cPL)-1)):
                    loopFlag += 1
                    curr = 0
                if loopFlag>1:
                    break
        x = x+1
            
    for x in range(0, len(copy_PL)):
        print("Process", copy_PL[x]['Process'],"Waiting Time :",sumW[x],", Turnaround Time: ", sumT[x])
    total1 = 0
    total2 = 0
    for i in sumW:
        total1 = total1 + i
    for i in sumT:
        total2 = total2 + i
    avg1 = round(total1/len(sumW), 2)
    avg2 = round(total2/len(sumT), 2)
    print("\nAverage Waiting Time: ", avg1, " Average Turnaround Time: ", avg2)
    print()

print("process1.txt and process2.txt are included in this project folder")
directory = input("Enter file directory [name of process file ie (process1.txt)]: ")
#"C:\\Users\Ardel\Documents\TextGenerator\game\process1.txt"
pL = readFile(directory)
#pL = readFile("C:\\Users\Ardel\Documents\TextGenerator\game\process1.txt")
FCFS(pL)
SJF(pL)
SRPT(pL)
Priority(pL)
RoundRobin(pL)
