#FirstFit and Performance Metrics by Ardel Bontilao
#WorstFit and BestFit by Kent Makibulan

import copy

def CreateJobList():
    entry = {'Job Stream #':1, 'Time':1, 'Job Size':1, 'Status': 0, 'Assigned Block': 0, 'Waiting': 0}
    time = [5,4,8,2,2,6,8,10,7,6,5,8,9,10,10,7,3,1,9,3,7,2,8,5,10]
    jobsize = [5760,4190,3290,2030,2550,6990,8940,740,3930,6890,6580,3820,9140,420,220,7540,3210,1380,9850,3610,7540,2710,8390,5950,760]
    jobList = []
    for i in range(1, len(jobsize)+1):
        entry['Job Stream #'] = i
        entry['Time'] = time[i-1]
        entry['Job Size'] = jobsize[i-1]
        jobList.append(entry)
        entry = {'Job Stream #':0, 'Time':0, 'Job Size':0, 'Status': 0, 'Assigned Block': 0, 'Waiting': 0}

    return jobList

def CreateMemoryList():
    entry = {'Memory Block':1, 'Size':1, 'Serving':0, 'Storage':0, 'Fragmentation':0, 'FragList':[]}
    memsize = [9500,7000,4500,8500,3000,9000,1000,5500,1500,500]
    memList = []
    for i in range(1, len(memsize)+1):
        entry['Memory Block'] = i
        entry['Size'] = memsize[i-1]
        memList.append(entry)
        entry = {'Memory Block':0, 'Size':0, 'Serving':0, 'Storage':0, 'Fragmentation':0, 'FragList':[]}

    return memList

def getMemSize(elem):
    return elem['Size']

def getMemBlock(elem):
    return elem.get('Memory Block')

def EmptyTime(JL):
    for i in range(0, len(JL)):
        if (JL[i]['Time'] != 0):
            return False
    return True

def FirstFit(JL,ML):
    print('*FIRST FIT*')
    JLcopy = copy.deepcopy(JL)
    MLcopy = copy.deepcopy(ML)
    time = 0
    execution = []
    waiting = []
    throughput = []
    queue = []
    max_size = max([x['Size'] for x in MLcopy])
    for i in range(len(JLcopy)):
        if JLcopy[i]['Job Size'] > max_size:
            JLcopy[i]['Assigned Block'] = None
            JLcopy[i]['Status'] = None
    unavailable = list(filter(lambda x: x['Status'] == None, JLcopy))
    print('Could not allocate Job#: ', [x['Job Stream #'] for x in unavailable])

    while True:
        print('\n==== Time:', time,'====')
        for i in range(len(execution)):
            execution[i]['Time'] -= 1
        done = list(filter(lambda x: x['Time'] == 0, execution))
        for i in range(len(done)):
            done[i]['Status'] = 1
            for j in range(len(MLcopy)):
                if MLcopy[j]['Memory Block'] == done[i]['Assigned Block']:
                    MLcopy[j]['Serving'] = 0
            print('  Finished Job#', done[i]['Job Stream #'])

        for i in MLcopy:
            if(i['Serving'] != 0):
                i['Storage'] += 1

        if 0 not in [x['Status'] for x in JLcopy]:
            break

        waiting = list(filter(lambda x: x['Assigned Block'] == 0, JLcopy))
        for i in range(len(waiting)):
            job = waiting[i]
            for j in range(len(MLcopy)):
                curr = MLcopy[j]
                if curr['Size'] >= job['Job Size'] and curr['Serving'] == 0:
                    MLcopy[j]['Serving'] = job['Job Stream #']
                    waiting[i]['Assigned Block'] = curr['Memory Block']
                    curr['Fragmentation'] = curr['Size'] - waiting[i]['Job Size']
                    curr['FragList'].append(curr['Fragmentation'])
                    print('  Added Job#', job['Job Stream #'])
                    job['Waiting'] = time
                    break

        execution = list(filter(lambda x: x['Assigned Block'] != 0 and x['Status'] == 0, JLcopy))
        waiting = list(filter(lambda x: x['Assigned Block'] == 0, JLcopy))
        print('    Execution:')
        for x in execution:
            print('    | Job#', x['Job Stream #'], 'at Memory Block', x['Assigned Block'])
        print('    Waiting:')
        for x in waiting:
            print('    _ Job#', x['Job Stream #'])
        print()

        print("\n>Throughput:", len(execution))
        throughput.append(len(execution))
        print(">Waiting Queue Length: ", len(waiting))
        queue.append(len(waiting))
        print(">Internal Fragmentation: ")
        for x in MLcopy:
            if (x['Serving'] != 0):
                print('  Memory Block',x['Memory Block'],'has leftover space of',x['Fragmentation'])
        time += 1
    print("\n+++ Performance +++")
    print(">Average Throughput:", round(sum(throughput)/len(throughput),2))
    percent = '%'
    h = 0
    r = 0
    i = 0
    z = 0
    for x in MLcopy:
        if(x['Storage']>(0.75*time) and x['Storage']<=(time)):
            h+=1
        if(x['Storage']>(0.5*time) and x['Storage']<=(0.75*time)):
            r+=1
        if(x['Storage']>(0.25*time) and x['Storage']<=(0.5*time)):
            i+=1
        if(x['Storage']>=(0) and x['Storage']<=(0.25*time)):
            z+=1
    heavy = round(((h/len(MLcopy))*100),2)
    reg = round(((r/len(MLcopy))*100),2)
    inf = round(((i/len(MLcopy))*100),2)
    zero = round(((z/len(MLcopy))*100),2)
    print(">Storage Utilization: "+str(heavy)+percent+" of partitions heavily used (75-100"+percent+" of runtime)")
    print(">Storage Utilization: "+str(reg)+percent+" of partitions regularly used (50-75"+percent+" of runtime)")
    print(">Storage Utilization: "+str(inf)+percent+" of partitions infrequently used (25-50"+percent+" of runtime)")
    print(">Storage Utilization: "+str(zero)+percent+" of partitions rarely used (0-25"+percent+" of runtime)")
    print('>Average Waiting Queue Length: ', round(sum(queue)/len(queue),2))
    print(">Waiting Time in Queue:" )
    wait = 0
    finished = list(filter(lambda x: x['Status'] == 1, JLcopy))
    for x in finished:
        print("  Job#",x['Job Stream #'], "waited for",x['Waiting'],"time units")
        wait = wait + x['Waiting']
    print(">Average Waiting Time:", round(wait/len(finished),2))
    print(">Average Internal Fragmentation of each block: ")
    totalIF = []
    fragged = list(filter(lambda x: x['FragList'], MLcopy))
    for x in fragged:
        avgIF = round(sum(x['FragList'])/len(x['FragList']),2)
        totalIF.append(avgIF)
        print('  Memory Block',x['Memory Block'],'average leftover space:', avgIF)
    print(">Average Internal Fragmentation: ", round(sum(totalIF)/len(totalIF),2))
    

def BestFit(JL,ML):
    print('*BEST FIT*')
    JLcopy = copy.deepcopy(JL)
    MLcopy = sorted(copy.deepcopy(ML), key=getMemSize)
    time = 0
    execution = []
    waiting = []
    throughput = []
    queue = []
    max_size = max([x['Size'] for x in MLcopy])
    for i in range(len(JLcopy)):
        if JLcopy[i]['Job Size'] > max_size:
            JLcopy[i]['Status'] = None
            JLcopy[i]['Assigned Block'] = None
            print(JLcopy[i]['Job Stream #'], 'cannot be executed')
    while True:
        print('\n === Time:', time,'===')

        for i in range(len(execution)):
            execution[i]['Time'] -= 1
        done = list(filter(lambda x: x['Time'] == 0, execution))
        for i in range(len(done)):
            done[i]['Status'] = 1
            for j in range(len(MLcopy)):
                if MLcopy[j]['Memory Block'] == done[i]['Assigned Block']:
                    MLcopy[j]['Serving'] = 0
            print('    Done', done[i]['Job Stream #'])

        for i in MLcopy:
            if(i['Serving'] != 0):
                i['Storage'] += 1

        if 0 not in [x['Status'] for x in JLcopy]:
            break

        waiting = list(filter(lambda x: x['Assigned Block'] == 0, JLcopy))
        for i in range(len(waiting)):
            job = waiting[i]
            for j in range(len(MLcopy)):
                curr = MLcopy[j]
                if curr['Size'] >= job['Job Size'] and curr['Serving'] == 0:
                    MLcopy[j]['Serving'] = job['Job Stream #']
                    MLcopy.sort(key=getMemSize)
                    waiting[i]['Assigned Block'] = curr['Memory Block']
                    curr['Fragmentation'] = curr['Size'] - waiting[i]['Job Size']
                    curr['FragList'].append(curr['Fragmentation'])
                    job['Waiting'] = time
                    print('    Added', job['Job Stream #'])
                    break

        execution = list(filter(lambda x: x['Assigned Block'] != 0 and x['Status'] == 0, JLcopy))
        waiting = list(filter(lambda x: x['Assigned Block'] == 0, JLcopy))
        print('    Execution:')
        for x in execution:
            print('    | Job#', x['Job Stream #'], 'at Memory Block', x['Assigned Block'])
        print('    Waiting:')
        for x in waiting:
            print('    _ Job#', x['Job Stream #'])
        print()
        print("\n>Throughput:", len(execution))
        throughput.append(len(execution))
        print(">Waiting Queue Length: ", len(waiting))
        queue.append(len(waiting))
        print(">Internal Fragmentation: ")
        for x in MLcopy:
            if (x['Serving'] != 0):
                print('  Memory Block',x['Memory Block'],'has leftover space of',x['Fragmentation'])
        time += 1
    
    print("\n+++ Performance +++")
    print(">Average Throughput:", round(sum(throughput)/len(throughput),2))
    percent = '%'
    h = 0
    r = 0
    i = 0
    z = 0
    for x in MLcopy:
        if(x['Storage']>(0.75*time) and x['Storage']<=(time)):
            h+=1
        if(x['Storage']>(0.5*time) and x['Storage']<=(0.75*time)):
            r+=1
        if(x['Storage']>(0.25*time) and x['Storage']<=(0.5*time)):
            i+=1
        if(x['Storage']>=(0) and x['Storage']<=(0.25*time)):
            z+=1
    heavy = round(((h/len(MLcopy))*100),2)
    reg = round(((r/len(MLcopy))*100),2)
    inf = round(((i/len(MLcopy))*100),2)
    zero = round(((z/len(MLcopy))*100),2)
    print(">Storage Utilization: "+str(heavy)+percent+" of partitions heavily used (75-100"+percent+" of runtime)")
    print(">Storage Utilization: "+str(reg)+percent+" of partitions regularly used (50-75"+percent+" of runtime)")
    print(">Storage Utilization: "+str(inf)+percent+" of partitions infrequently used (25-50"+percent+" of runtime)")
    print(">Storage Utilization: "+str(zero)+percent+" of partitions rarely used (0-25"+percent+" of runtime)")
    print('>Average Waiting Queue Length: ', round(sum(queue)/len(queue),2))
    print(">Waiting Time in Queue:" )
    wait = 0
    finished = list(filter(lambda x: x['Status'] == 1, JLcopy))
    for x in finished:
        print("  Job#",x['Job Stream #'], "waited for",x['Waiting'],"time units")
        wait = wait + x['Waiting']
    print(">Average Waiting Time:", round(wait/len(finished),2))
    print(">Average Internal Fragmentation of each block: ")
    totalIF = []
    MLcopy.sort(key=getMemBlock)
    fragged = list(filter(lambda x: x['FragList'], MLcopy))
    for x in fragged:
        avgIF = round(sum(x['FragList'])/len(x['FragList']),2)
        totalIF.append(avgIF)
        print('  Memory Block',x['Memory Block'],'average leftover space:', avgIF)
    print(">Average Internal Fragmentation: ", round(sum(totalIF)/len(totalIF),2))

def WorstFit(JL,ML):
    print('*WORST FIT*')
    JLcopy = copy.deepcopy(JL)
    MLcopy = sorted(copy.deepcopy(ML),key=getMemSize, reverse=True)
    time = 0
    execution = []
    waiting = []
    throughput = []
    queue = []
    max_size = max([x['Size'] for x in MLcopy])
    for i in range(len(JLcopy)):
        if JLcopy[i]['Job Size'] > max_size:
            JLcopy[i]['Status'] = None
            JLcopy[i]['Assigned Block'] = None
            print(JLcopy[i]['Job Stream #'], 'cannot be executed')
    while True:
        print('\n=== Time:', time,'===')

        for i in range(len(execution)):
            execution[i]['Time'] -= 1
        done = list(filter(lambda x: x['Time'] == 0, execution))
        for i in range(len(done)):
            done[i]['Status'] = 1
            for j in range(len(MLcopy)):
                if MLcopy[j]['Memory Block'] == done[i]['Assigned Block']:
                    MLcopy[j]['Serving'] = 0
            print('  Finished Job#', done[i]['Job Stream #'])

        for i in MLcopy:
            if(i['Serving'] != 0):
                i['Storage'] += 1

        if 0 not in [x['Status'] for x in JLcopy]:
            break

        waiting = list(filter(lambda x: x['Assigned Block'] == 0, JLcopy))
        for i in range(len(waiting)):
            job = waiting[i]
            for j in range(len(MLcopy)):
                curr = MLcopy[j]
                if curr['Size'] >= job['Job Size'] and curr['Serving'] == 0:
                    MLcopy[j]['Serving'] = job['Job Stream #']
                    MLcopy.sort(key=getMemSize, reverse=True)
                    waiting[i]['Assigned Block'] = curr['Memory Block']
                    curr['Fragmentation'] = curr['Size'] - waiting[i]['Job Size']
                    curr['FragList'].append(curr['Fragmentation'])
                    job['Waiting'] = time
                    print('  Added Job#', job['Job Stream #'])
                    break

        execution = list(filter(lambda x: x['Assigned Block'] != 0 and x['Status'] == 0, JLcopy))
        waiting = list(filter(lambda x: x['Assigned Block'] == 0, JLcopy))
        print('    Execution:')
        for x in execution:
            print('    | Job#', x['Job Stream #'], 'at Memory Block', x['Assigned Block'])
        print('    Waiting:')
        for x in waiting:
            print('    _ Job#', x['Job Stream #'])
        print()
        print("\n>Throughput:", len(execution))
        throughput.append(len(execution))
        print(">Waiting Queue Length: ", len(waiting))
        queue.append(len(waiting))
        print(">Internal Fragmentation: ")
        for x in MLcopy:
            if (x['Serving'] != 0):
                print('  Memory Block',x['Memory Block'],'has leftover space of',x['Fragmentation'])
        time += 1

    print("\n+++ Performance +++")
    print(">Average Throughput:", round(sum(throughput)/len(throughput),2))
    percent = '%'
    h = 0
    r = 0
    i = 0
    z = 0
    for x in MLcopy:
        if(x['Storage']>(0.75*time) and x['Storage']<=(time)):
            h+=1
        if(x['Storage']>(0.5*time) and x['Storage']<=(0.75*time)):
            r+=1
        if(x['Storage']>(0.25*time) and x['Storage']<=(0.5*time)):
            i+=1
        if(x['Storage']>=(0) and x['Storage']<=(0.25*time)):
            z+=1
    heavy = round(((h/len(MLcopy))*100),2)
    reg = round(((r/len(MLcopy))*100),2)
    inf = round(((i/len(MLcopy))*100),2)
    zero = round(((z/len(MLcopy))*100),2)
    print(">Storage Utilization: "+str(heavy)+percent+" of partitions heavily used (75-100"+percent+" of runtime)")
    print(">Storage Utilization: "+str(reg)+percent+" of partitions regularly used (50-75"+percent+" of runtime)")
    print(">Storage Utilization: "+str(inf)+percent+" of partitions infrequently used (25-50"+percent+" of runtime)")
    print(">Storage Utilization: "+str(zero)+percent+" of partitions rarely used (0-25"+percent+" of runtime)")
    print('>Average Waiting Queue Length: ', round(sum(queue)/len(queue),2))
    print(">Waiting Time in Queue:" )
    wait = 0
    finished = list(filter(lambda x: x['Status'] == 1, JLcopy))
    for x in finished:
        print("  Job#",x['Job Stream #'], "waited for",x['Waiting'],"time units")
        wait = wait + x['Waiting']
    print(">Average Waiting Time:", round(wait/len(finished),2))
    print(">Average Internal Fragmentation of each block: ")
    totalIF = []
    MLcopy.sort(key=getMemBlock)
    fragged = list(filter(lambda x: x['FragList'], MLcopy))
    for x in fragged:
        avgIF = round(sum(x['FragList'])/len(x['FragList']),2)
        totalIF.append(avgIF)
        print('  Memory Block',x['Memory Block'],'average leftover space:', avgIF)
    print(">Average Internal Fragmentation: ", round(sum(totalIF)/len(totalIF),2))
            


JL = CreateJobList()
ML = CreateMemoryList()
while(True):
    val = input("1-First Fit... 2-Worst Fit... 3-Best Fit:\n")
    if val == '1':
        print('--------------------')
        FirstFit(JL,ML)
    if val == '2':
        print('--------------------')
        WorstFit(JL,ML)
    if val == '3':
        print('--------------------')
        BestFit(JL,ML)



