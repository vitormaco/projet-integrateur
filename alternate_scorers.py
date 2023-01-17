import math
import numpy as np

def geometric_mean(data):
    x = np.prod(data)
    res = math.exp(math.log(x)/len(data))
    return res

def mid_range(data):
    return 0.5*(max(data)+min(data))

def harmonic_mean(data):
    divide = np.sum(1/data)
    return len(data)/divide

def lehmer_mean(data,powerRange:tuple):
    f = lambda x : np.sum(data**x)
    return [f(i-1)/f(i) for i in range(powerRange[0],powerRange[1])]






# scoreTimePriority -> dict with range as string as key and factor as value
# Key -> '5-8' '9- '
# nodePriorities -> dict with node as key and factor as value
# data represents the whole database in a json format
# the json uses a node id per key
def peerTrust(data,alpha=1,beta=1,nodePriorities=None,scoreTimePriority=None,epsilon=0.2,delta=5):

    mode = 0
    # Check if no priorities
    if scoreTimePriority:
        mode = 2
        scoreTimeFactorList = []
        for key in scoreTimePriority:
            start = key[0]
            end = key[-1]
            startIndex = 0
            endIndex = len(data[0]["ram"])
            if start != " ":
                startIndex = int(start)
            if end != " ":
                endIndex = int(end)
            for _ in range(startIndex,endIndex):
                scoreTimeFactorList.append(scoreTimePriority[key])

    if nodePriorities:
        # if time priorities exists the mode will be update too
        mode += 1

    nodeScore = dict()
    for node in data:
        nodeScore[node] = dict()

        histSize = len(data[0]["ram"])

        sumRam = 0
        sumRamSmall = 0
        sumCpu = 0
        sumCpuSmall = 0

        for i in range(histSize):
            if not data[node]["ram"][i]:
                data[node]["ram"][i] = 0
            if not data[node]["cpu"][i]:
                data[node]["cpu"][i] = 0

            # Compute scores on the whole window and a reduced window
            sumRam += data[node]["ram"][i] * scoreTimeFactorList[i] + (beta*nodePriorities[node])
            sumCpu += data[node]["cpu"][i] * scoreTimeFactorList[i] + (beta*nodePriorities[node])
            if ( abs(histSize - i ) < delta):
                sumRamSmall += data[node]["ram"][i]*scoreTimeFactorList[i] + (beta*nodePriorities[node])
                sumCpuSmall += data[node]["cpu"][i]*scoreTimeFactorList[i] + (beta*nodePriorities[node])

        if abs(sumCpu-sumCpuSmall) > epsilon:
            resCpu = sumCpuSmall
        else:
            resCpu = sumCpu
        if abs(sumRam-sumRamSmall) > epsilon:
            resRam = sumRamSmall
        else:
            resRam = sumRam

        print("index = ",node)
        nodeScore[node]["cpu_score"] = (alpha * resCpu)/histSize
        nodeScore[node]["ram_score"] = (alpha * resRam)/histSize

    return nodeScore



def test():
    data = {
        0 : {
            "cpu" : [0.2,0.8,0.5,0.2,0.2,0.2,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.1,0.1],
            "ram" : [0.2,0.8,0.5,0.2,0.2,0.2,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.1,0.1],
            "cpu_score" : 0.5,
            "ram_score" : 0.5
        },

        1 : {
            "cpu" : [0.2,0.8,0.5,0.2,0.2,0.2,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.1,0.1],
            "ram" : [0.2,0.8,0.5,0.2,0.2,0.2,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.1,0.1],
            "cpu_score" : 0.5,
            "ram_score" : 0.5
        },

        2 : {
            "cpu" : [0.2,0.8,0.5,0.2,0.2,0.2,0.8,0.8,0.8,0.8,0.8,0.8,0.7,0.7,0.7],
            "ram" : [0.2,0.8,0.5,0.2,0.2,0.2,0.8,0.8,0.8,0.8,0.8,0.8,0.7,0.7,0.7],
            "cpu_score" : 0.5,
            "ram_score" : 0.5
        }

    }

    prioNode = [1,1,1]
    prioTime = {
        " -4" : 0.1,
        "4- " : 1
    }

    res = peerTrust(data,nodePriorities=prioNode,scoreTimePriority=prioTime)
    print(res)

test()