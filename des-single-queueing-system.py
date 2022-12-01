################################################
# Veit Ebbers
# 11/29/2022
# Project 4
################################################

import pandas as pd
import numpy as np
import itertools

# user input
endTime = input("Enter end time:")
print("End time: " + endTime)
endTime=int(endTime)

debugMode = input("Debug mode? (y/n): ")
if debugMode == "y": 
    print("Debug mode is on")
elif debugMode == "n":
    print("Debug mode is off")
else :
    print("Invalid input! Please enter y or n. Debug mode is off.")

# create all possible combinations of arrival and departure times
### create arrival times
def simulate(time):
    
    # generate time between arrivals discrete numbers from 1 to 8
    def randomArrivalTime():
        return int(np.random.choice(np.arange(1, 9), p=[0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125]))
    
    #generate service time discrete numbers 1 to 6
    def randomServiceTime():
        return int(np.random.choice(np.arange(1, 7), p=[0.1, 0.2, 0.3, 0.25, 0.1, 0.05]))
    
    
    # compute ordered event list
    
    clock = 0
    lst=1
    lqt=0
    i=0
    arrivalTime=randomArrivalTime()
    serviceTime=randomServiceTime()
    
    arrivalTimes=np.array([])
    departureTimes=np.array([])
    
        
    if arrivalTime<serviceTime:
        departureTime=serviceTime
    else:
        departureTime=arrivalTime

    
    arrivalTimes=np.append(arrivalTimes,arrivalTime)
    departureTimes=np.append(departureTimes,departureTime)
    
    
    while arrivalTime < time:
        
        i+=1
        arrivalTime+=randomArrivalTime()
        serviceTime=randomServiceTime()
        
        if arrivalTime>departureTime:
            departureTime=arrivalTime+serviceTime
        else:
            departureTime+=serviceTime
            
        if arrivalTime<departureTime:
            lst=1
        else:
            lst=0
            
        arrivalTimes=np.append(arrivalTimes,arrivalTime)
        departureTimes=np.append(departureTimes,departureTime)      
    
    # create key value pairs for A and D
    arrivalValues = ['A' for i in range(len(arrivalTimes))]
    departureValues = ['D' for i in range(len(departureTimes))]
    
    arrivalTimesMap = {arrivalTimes[i]: arrivalValues[i] for i in range(len(arrivalTimes))}
    departureTimesMap = {departureTimes[i]: departureValues[i] for i in range(len(departureTimes))}
    
    allTimes=arrivalTimesMap|departureTimesMap
    orderedList=sorted(allTimes.items())
    
        
    return orderedList,arrivalTimes,departureTimes,allTimes

orderedList,arrivalTimes,departureTimes,allTimes = simulate(endTime)

# compute statistics
def calculateTable(orderedList,arrivalTimes,departureTimes,allTimes,time):

    df=pd.DataFrame(columns=['Type','Clock','LQ(t)','LS(t)','Future Event List','Busy','Max Queue'])
    
    # calculate LS(t)
    def lstHelper(x):
        lst=0
        if x=='A':
            lst=1
        else: 
            lst=0
        return lst
    
    # calculate LQ(t) and future event list
    def futureEventListHelper(x,y):
        res =[]
        lqt =[]
        
        for i in range(0,len(x)-2,1):

            try:
                cool = res[i-1][0][1]
            except IndexError:
                cool = 0
            try:
                cool2 = res[i-1][1][1]
            except IndexError:
                cool2 = 1
            
            if x[i-1][1]=='A' and x[i][1]=='A' and cool<cool2:
                lqtValue=1
                lqt.append(lqtValue)
                newValue = [(x[i+1][1],x[i+1][0]),(x[i+2][1],x[i+2][0]),('E',y)]
                res.append(newValue)
            elif x[i+1][1]=='D' and x[i+2][1]=='A':
                lqtValue=0
                lqt.append(lqtValue)
                newValue = [(x[i+1][1],x[i+1][0]),(x[i+2][1],x[i+2][0]),('E',y)]
                res.append(newValue)
            elif x[i+1][1]=='A' and x[i+2][1]=='D':
                lqtValue=0
                lqt.append(lqtValue)
                newValue = [(x[i+1][1],x[i+1][0]),(x[i+2][1],x[i+2][0]),('E',y)]
                res.append(newValue)
            elif x[i+1][1]=='A' and x[i+2][1]=='A':
                lqtValue=0
                lqt.append(lqtValue)
                newValue = [(x[i+1][1],x[i+1][0]),(x[i+2][1],x[i+2][0]),('E',y)]
                res.append(newValue)
            
        return res,lqt
    
    # calculate busy list
    def busyHelper(eventList,orderedList):
        busyList=[]
        busy=0
        
        for i in range(0,len(eventList),1):
            if orderedList[i-1][1]=='A' and eventList[i-1][0][0]=='D':
                res1=int(res[i-1][0][1])
                res2=int(orderedList[i-1][0])
                busy=res1-res2
                if busy<0:
                    busy=0
                busyList.append(busy)
            elif orderedList[i-1][1]=='A' and eventList[i-1][0][0]=='A':
                res1=int(res[i-1][0][1])
                res2=int(orderedList[i-1][0])
                busy=res1-res2
                if busy<0:
                    busy=0
                busyList.append(busy)
            elif orderedList[i-1][1]=='D' and eventList[i-1][0][0]=='D':
                res1=int(res[i-1][0][1])
                res2=int(orderedList[i-1][0])
                busy=res1-res2
                if busy<0:
                    busy=0
                busyList.append(busy)
            else:
                busyList.append(0)
        
        return busyList
    
    

    res,lqt = futureEventListHelper(orderedList,time)
    busyList = busyHelper(res,orderedList)
    
    #receive results and put them in table
    for i in range(0,len(res),1):
        try:
            departureData = res[i][0]
        except IndexError:
            departureData = 0
        
        df.loc[i, 'Type'] = orderedList[i][1]
        df.loc[i, 'Clock'] = orderedList[i][0]
        df.loc[i, 'LQ(t)'] = lqt[i]
        df.loc[i, 'LS(t)'] = lstHelper(orderedList[i][1])
        df.loc[i, 'Future Event List'] = res[i][0],res[i][1],res[i][2]
        df.loc[i, 'Busy'] = np.cumsum(busyList)[i]
        df.loc[i, 'Max Queue'] = np.cumsum(lqt)[i]
    
    return df,res, busyList,lqt,orderedList,busyList

df,res,busyList,lqt,orderedList,busyList = calculateTable(orderedList,arrivalTimes,departureTimes,allTimes,endTime)

# plot table
if debugMode == "y":
    print(df.head())
    print(df.tail())
    

idleTime=orderedList[len(busyList)-1][0]-np.cumsum(busyList)[-1]
maxQueueLength=max(np.cumsum(lqt))
# print results
print("IDLE time: ",idleTime)
print("Max Queue Length: ",maxQueueLength)