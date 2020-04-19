import sys
import numpy as np
import pandas as pd


# Decision of the current day by the current price, with 3 modifiable parameters
def myStrategy(pastPriceVec, currentPrice, windowSize, alpha, beta,rsi_tp):
	action=0		# action=1(buy), -1(sell), 0(hold), with 0 as the default action
	import numpy as np
	import talib
	dataLen=len(pastPriceVec)		# Length of the data vector
	if dataLen==0:
		return action
	############## RSI #####################
	if len(pastPriceVec)>rsi_tp:
		rsi = talib.RSI(pastPriceVec, timeperiod=rsi_tp)
		if rsi[len(rsi)-1]>70:
			action = -1
		elif rsi[len(rsi)-1]<30:
			action = 1
	############## whole RSI #####################
	#rsiL = talib.RSI(pastPriceVec, timeperiod=rsiL)
	#rsiSNow = talib.RSI(pastPriceVec, timeperiod=rsiS)
	#rsiSLast = talib.RSI(pastPriceVec[0:len(pastPriceVec)-2], timeperiod=rsiS)

	#if rsiSNow[len(rsiSNow)-1]>rsiL[len(rsiL)-1] and rsiL[len(rsiL)-1]>rsiSLast[len(rsiSLast)-1]:
	#	action = 1
	#elif rsiSNow[len(rsiSNow)-1]<rsiL[len(rsiL)-1] and rsiL[len(rsiL)-1]<rsiSLast[len(rsiSLast)-1]:
	#	action =-1
	############# moving average #############
	# Compute ma
	if dataLen<windowSize:
		ma=np.mean(pastPriceVec)	# If given price vector is small than windowSize, compute MA by taking the average
	else:
		windowedData=pastPriceVec[-windowSize:]		# Compute the normal MA using windowSize
		ma=np.mean(windowedData)
	# Determine action
	if (currentPrice-ma)>alpha:		# If price-ma > alpha ==> buy
		action=1
	elif (currentPrice-ma)<-beta:	# If price-ma < -beta ==> sell
		action=-1
	return action



# Compute return rate over a given price vector, with 3 modifiable parameters
def computeReturnRate(priceVec, windowSize, alpha, beta,rsi_tp):
	capital=1000	# Initial available capital
	capitalOrig=capital	 # original capital
	dataCount=len(priceVec)				# day size
	suggestedAction=np.zeros((dataCount,1))	# Vec of suggested actions
	stockHolding=np.zeros((dataCount,1))  	# Vec of stock holdings
	total=np.zeros((dataCount,1))	 	# Vec of total asset
	realAction=np.zeros((dataCount,1))	# Real action, which might be different from suggested action. For instance, when the suggested action is 1 (buy) but you don't have any capital, then the real action is 0 (hold, or do nothing). 
	# Run through each day
	for ic in range(dataCount):
		currentPrice=priceVec[ic]	# current price
		suggestedAction[ic]=myStrategy(priceVec[0:ic], currentPrice, windowSize, alpha, beta,rsi_tp)		# Obtain the suggested action
		# get real action by suggested action
		if ic>0:
			stockHolding[ic]=stockHolding[ic-1]	# The stock holding from the previous day
		if suggestedAction[ic]==1:	# Suggested action is "buy"
			if stockHolding[ic]==0:		# "buy" only if you don't have stock holding
				stockHolding[ic]=capital/currentPrice # Buy stock using cash
				capital=0	# Cash
				realAction[ic]=1
		elif suggestedAction[ic]==-1:	# Suggested action is "sell"
			if stockHolding[ic]>0:		# "sell" only if you have stock holding
				capital=stockHolding[ic]*currentPrice # Sell stock to have cash
				stockHolding[ic]=0	# Stocking holding
				realAction[ic]=-1
		elif suggestedAction[ic]==0:	# No action
			realAction[ic]=0
		else:
			assert False
		total[ic]=capital+stockHolding[ic]*currentPrice	# Total asset, including stock holding and cash 
	returnRate=(total[-1]-capitalOrig)/capitalOrig		# Return rate of this run
	return returnRate

if __name__=='__main__':
	returnRateBest=-1.00	 # Initial best return rate
	df=pd.read_csv(sys.argv[1])	# read stock file
	adjClose=df["Adj Close"].values		# get adj close as the price vector
	windowSizeMin=26; windowSizeMax=26;	# Range of windowSize to explore
	alphaMin=0; alphaMax=0;			# Range of alpha to explore
	betaMin=2; betaMax=2;
	rsi_tpMin=9; rsi_tpMax=100;
	# Range of beta to explore
	# Start exhaustive search
	for windowSize in range(windowSizeMin, windowSizeMax+1):		# For-loop for windowSize
		print("windowSize=%d" %(windowSize))
		for alpha in range(alphaMin, alphaMax+1):	    	# For-loop for alpha
			print("\talpha=%d" %(alpha))
			for beta in range(betaMin, betaMax+1):		# For-loop for beta
				if beta>alpha:
					print("\t\tbeta=%d" %(beta))	# No newline
					for rsi_tp in range(rsi_tpMin, rsi_tpMax+1):
						print("\trsi timep=%d" %(rsi_tp), end="")
						returnRate=computeReturnRate(adjClose, windowSize, alpha, beta,rsi_tp)		# Start the whole run with the given parameters
						print(" ==> returnRate=%f " %(returnRate))
						if returnRate > returnRateBest:		# Keep the best parameters
							windowSizeBest=windowSize
							alphaBest=alpha
							betaBest=beta
							rsi_tpBest=rsi_tp
							returnRateBest=returnRate
	print("Best settings: windowSize=%d, alpha=%d, beta=%d, rsi_tp=%d ==> returnRate=%f" %(windowSizeBest,alphaBest,betaBest,rsi_tpBest,returnRateBest))		# Print the best result
