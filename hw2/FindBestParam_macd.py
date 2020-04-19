import sys
import numpy as np
import pandas as pd
import talib

# Decision of the current day by the current price, with 3 modifiable parameters
def myStrategy(pastPriceVec, currentPrice,fp,sp,sigp):
	import numpy as np
	action=0		# action=1(buy), -1(sell), 0(hold), with 0 as the default action
	################## macd ###################
	if len(pastPriceVec)>sp:
		macd, signal, hist = talib.MACD(pastPriceVec, fastperiod=fp, slowperiod=sp, signalperiod=sigp)

		macdL = macd.tolist()
		signalL = signal.tolist()

		if macdL[len(macdL)-1]<0 and macdL[len(macdL)-2]>0 and signalL[len(signalL)-1]<0:
			action = -1
		elif macdL[len(macdL)-1]>0 and macdL[len(macdL)-2]<0 and signalL[len(signalL)-1]>0:
			action = 1
		if abs((macdL[len(macdL)-1]-signalL[len(signalL)-1]))<1:
			if macdL[len(macdL)-1]<signalL[len(signalL)-2] and signalL[len(signalL)-2]>0 and macdL[len(macdL)-1]>0:
				aciton = 1
			elif macdL[len(macdL)-1]>signalL[len(signalL)-2] and macdL[len(macdL)-1]<0 and signalL[len(signalL)-2]<0:
				action = -1

	
	return action

# Compute return rate over a given price vector, with 3 modifiable parameters
def computeReturnRate(priceVec, windowSize, alpha, beta,fp,sp,sigp):
	capital=1000													# Initial available capital
	capitalOrig=capital	 										# original capital
	dataCount=len(priceVec)								# day size
	suggestedAction=np.zeros((dataCount,1))			# Vec of suggested actions
	stockHolding=np.zeros((dataCount,1))  			# Vec of stock holdings
	total=np.zeros((dataCount,1))	 						# Vec of total asset
	realAction=np.zeros((dataCount,1))					# Real action, which might be different from suggested action. For instance, when the suggested action is 1 (buy) but you don't have any capital, then the real action is 0 (hold, or do nothing). 
	# Run through each day
	for ic in range(dataCount):
		currentPrice=priceVec[ic]							# current price
		suggestedAction[ic]=myStrategy(priceVec[0:ic], currentPrice, windowSize, alpha, beta,fp,sp,sigp)		# Obtain the suggested action
		# get real action by suggested action
		if ic>0:
			stockHolding[ic]=stockHolding[ic-1]			# The stock holding from the previous day
		if suggestedAction[ic]==1:							# Suggested action is "buy"
			if stockHolding[ic]==0:							# "buy" only if you don't have stock holding
				stockHolding[ic]=capital/currentPrice 	# Buy stock using cash
				capital=0											# Cash
				realAction[ic]=1
		elif suggestedAction[ic]==-1:						# Suggested action is "sell"
			if stockHolding[ic]>0:								# "sell" only if you have stock holding
				capital=stockHolding[ic]*currentPrice 	# Sell stock to have cash
				stockHolding[ic]=0								# Stocking holding
				realAction[ic]=-1
		elif suggestedAction[ic]==0:							# No action
			realAction[ic]=0
		else:
			assert False
		total[ic]=capital+stockHolding[ic]*currentPrice	# Total asset, including stock holding and cash 
	returnRate=(total[-1]-capitalOrig)/capitalOrig		# Return rate of this run
	return returnRate

if __name__=='__main__':
	returnRateBest=-1.00	 									# Initial best return rate
	df=pd.read_csv(sys.argv[1])								# read stock file
	adjClose=df["close"].values								# get adj close as the price vector
	fpMin=12; fpMax=30;										# Range of windowSize to explore
	spMin=26; spMax=40;										# Range of alpha to explore
	sigpMin=9; sigpMax=20;									# Range of beta to explore


	# Start exhaustive search
	for f in range(fpMin, fpMax+1):							# For-loop for windowSize
		print("fastperiod=%d" %(f))
		for s in range(spMin, spMax+1):	    			# For-loop for alpha
			print("\tslowperiod=%d" %(s))
			for sig in range(sigpMin, sigpMax+1):			# For-loop for beta
				print("\t\tsignalperiod=%d" %(sig), end="")	# No newline
				if(sig<f and f<s):
					returnRate=computeReturnRate(adjClose,f,s,sig)		# Start the whole run with the given parameters
					print(" ==> returnRate=%f " %(returnRate))
					if returnRate > returnRateBest:			# Keep the best parameters
						fastPeriodBest=f
						slowPeriodBest=s
						signalPeriodBest=sig
						returnRateBest=returnRate
	print("Best settings: fastperiod=%d, slowperiod=%d, signalperiod=%d ==> returnRate=%f" %(fastPeriodBest,slowPeriodBest,signalPeriodBest,returnRateBest))		# Print the best result
