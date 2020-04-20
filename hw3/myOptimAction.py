import numpy as np

def myOptimAction(priceMat, transFeeRate):
    # Explanation of my approach:
	# 1. Technical indicator used: Watch next day price
	# 2. if next day price > today price + transFee ==> buy
    #       * buy the best stock
	#    if next day price < today price + transFee ==> sell
    #       * sell if you are holding stock
    # 3. You should sell before buy to get cash each day
    # default
    cash = 1000
    p = 0.01 #transaction fee
    dataLen, n = priceMat.shape  # day size & stock count   
    dpVec = np.zeros((dataLen,n+1))  # Mat of stock holdings
    path = np.zeros((dataLen,n+1))

    #save my dp
    for i in range(0,dataLen):
        for j in range(0,n):
            path[i][j]=-1
        if i==0:
            dpVec[i][0]=cash
            for s in range(0,n):
                dpVec[i][s+1]=round(dpVec[i][0]/priceMat[i][s])
        else:
            for s in range(0,n): #calculate cash
                tempCash = round(priceMat[i][s]*dpVec[i-1][s+1])
                if tempCash*(1-transFeeRate)>dpVec[i-1][0]: #if sell stock
                    dpVec[i][0]=tempCash
                    path[i][0]=s
                elif dpVec[i][0]==0: #if didn't sell any stock
                    dpVec[i][0]=dpVec[i-1][0]
            for s in range(0,n): #see if buy
                    tempStock = round(dpVec[i][0]/priceMat[i][s])
                    if(tempStock*(1-transFeeRate)>dpVec[i-1][s+1] and path[i][0]==-1):
                        dpVec[i][s+1] = tempStock;
                        path[i][s+1]=n+1 #stock was brought with original cash
                    elif (tempStock*(1-transFeeRate)*(1-transFeeRate)>dpVec[i-1][s+1] and path[i][0]!=-1):
                        dpVec[i][s+1] = tempStock;
                        path[i][s+1]=path[i][0]
                    else:
                        dpVec[i][s+1] = dpVec[i-1][s+1]
                        path[i][s+1] = s
    #print(path)
    #create actionMat
    actionAll = np.zeros((dataLen,4))
    #action = [day, sellStock[i], -1, sellPrice[i]]
    #actionMat.append( action )
    currPos=0
    for i in range(dataLen-1, -1, -1):
        #print(i,currPos)
        currPos=int(currPos)
        #print(currPos)
        if(currPos==n+1):
            currPos=0
        for j in range(0,4):
            actionAll[i][j]=-1
        #for cash
        if(currPos==0 and path[i][0]!=n+1):#not come from myself
            actionAll[i][0]=i
            actionAll[i][1]=path[i][currPos]
            actionAll[i][2]=-1
            actionAll[i][3]=dpVec[i][0]
            currPos=path[i][currPos]+1
            #print("in pos=0")

        #for stock
        elif(currPos!=path[i][currPos]+1):#not come from myself
            if(path[i][currPos]==n+1):#no sell, buy
                actionAll[i][0]=i
                actionAll[i][1]=-1
                actionAll[i][2]=currPos-1
                actionAll[i][3]=dpVec[i][currPos]*priceMat[i][currPos-1]
                currPos=0
                #print("in no sell, buy")
            else:#sell and buy
                actionAll[i][0]=i
                actionAll[i][1]=path[i][currPos]
                actionAll[i][2]=currPos-1
                actionAll[i][3]=dpVec[i][currPos]*priceMat[i][currPos-1]
                currPos=path[i][currPos]+1
                #print("in sell and buy")


    actionMat = []
    for i in range(0, dataLen):
        if(actionAll[i][1]==-1 and actionAll[i][2] == -1):
            i=i
        elif(actionAll[i][0]!=-1 and i!=0 ):
            action = [int(actionAll[i][0]), int(actionAll[i][1]), int(actionAll[i][2]), int(actionAll[i][3])]
            actionMat.append( action )
    #print(actionMat)
    return actionMat


    