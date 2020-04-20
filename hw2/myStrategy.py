def myStrategy(pastData, currPrice, stockType):
	import talib
	import numpy as np
	import pandas as pd
	action = 0 # action=1(buy), -1(sell), 0(hold), with 0 as the default action
	paramSetting={'SPY': {'alpha':6, 'beta':15, 'windowSize':4, 'rsi_tp':96, 'fastperiod':0, 'slowperiod':0, 'signalperiod':0, 'rsiL':0, 'rsiS':0},
					'IAU': {'alpha':0, 'beta':2, 'windowSize':24,'rsi_tp':0, 'fastperiod':13, 'slowperiod':24, 'signalperiod':12, 'rsiL':0, 'rsiS':0},
					'LQD': {'alpha':0, 'beta':1, 'windowSize':5,'rsi_tp':59, 'fastperiod':23, 'slowperiod':26, 'signalperiod':19, 'rsiL':22, 'rsiS':16},
					'DSI': {'alpha':2, 'beta':10, 'windowSize':17,'rsi_tp':59, 'fastperiod':0, 'slowperiod':0, 'signalperiod':0, 'rsiL':0, 'rsiS':0}}
	windowSize=paramSetting[stockType]['windowSize']
	alpha=paramSetting[stockType]['alpha']
	beta=paramSetting[stockType]['beta']
	rsi_tp=paramSetting[stockType]['rsi_tp']
	fp=paramSetting[stockType]['fastperiod']
	sp=paramSetting[stockType]['slowperiod']
	sigp=paramSetting[stockType]['signalperiod']
	rsiL=paramSetting[stockType]['rsiL']
	rsiS=paramSetting[stockType]['rsiS']



	
	############## RSI #####################
	if len(pastData)>rsi_tp and (stockType=='SPY'  ):
		rsi = talib.RSI(pastData, timeperiod=rsi_tp)
		if rsi[len(rsi)-1]>70:
			action = -1
		elif rsi[len(rsi)-1]<30:
			action = 1

	############### whole rsi ##################

	#if  len(pastData)>rsiL :
	#	rsiL = talib.RSI(pastData, timeperiod=rsiL)
	#	rsiSNow = talib.RSI(pastData, timeperiod=rsiS)
	#	rsiSLast = talib.RSI(pastData[0:len(pastData)-2], timeperiod=rsiS)

	#	if rsiSNow[len(rsiSNow)-1]>rsiL[len(rsiL)-1] and rsiL[len(rsiL)-1]>rsiSLast[len(rsiSLast)-1]:
	#		action = 1
	#	elif rsiSNow[len(rsiSNow)-1]<rsiL[len(rsiL)-1] and rsiL[len(rsiL)-1]<rsiSLast[len(rsiSLast)-1]:
	#		action =-1


	################## macd ###################
	if len(pastData)>sp and (stockType=='IAU'):
		macd, signal, hist = talib.MACD(pastData, fastperiod=fp, slowperiod=sp, signalperiod=sigp)

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
	############## moving ave ####################
	# action = 0 or 1 or -1
	
	
	if stockType=='SPY' or stockType=='IAU' or stockType=='LQD' or stockType=='DSI' :
		dataLen=len(pastData)		# Length of the data vector
		if dataLen==0: 
			return action
		# Compute MA
		if dataLen<windowSize:
			ma=np.mean(pastData)	# If given price vector is small than windowSize, compute MA by taking the average
		else:
			windowedData=pastData[-windowSize:]		# Compute the normal MA using windowSize 
			ma=np.mean(windowedData)
		# Determine action
		if (currPrice-ma)>alpha:		# If price-ma > alpha ==> buy
			action=1
		elif (currPrice-ma)<-beta:	# If price-ma < -beta ==> sell
			action=-1
	


	return action
