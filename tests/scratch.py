import cbpro
import pandas as pd
import time 
import datetime as dt
import numpy as np
from tools_test import get_CurrentPrice,get_SpecificAccount

def main():

	path = str(input("Enter the directory where your API Keys are: "))
	df = pd.read_csv(path)
	keys = df.columns.values
	key = keys[0]
	secret = keys[1]
	passphrase = keys[2]
	checkPrice = True
	currency = 'BTC-USD'

	# Granularity (in seconds). So 300 = data from every 5 min (300s/60s = 5 mins)
	period = 60
	auth_client = cbpro.AuthenticatedClient(key,secret,passphrase)
	# Get the currency's specific ID
	specificID = get_SpecificAccount(auth_client,currency[:3])
	print(specificID)
	# currentPrice = []
	j = 0
	while j < 500:
		currentPrice,closing_price_array = get_CurrentPrice(auth_client,currency,period)
		time.sleep(1)
		avg_closing_price = []
		avg_closing_price.append(np.mean(closing_price_array))
		upPrices = []
		downPrices = []
		i = 0
		while i < len(avg_closing_price):
			if i == 0:
				upPrices.append(0)
				downPrices.append(0)
			else:
				if (avg_closing_price[i]-avg_closing_price[i-1] ) > 0:
					upPrices.append(avg_closing_price[i]-avg_closing_price[i-1])
					downPrices.append(0)
				else:
					downPrices.append(avg_closing_price[i]-avg_closing_price[i-1])
					upPrices.append(0)
			i += 1
		x = 0
		avg_gain = []
		avg_loss = []
		#  Loop to calculate the average gain and loss
		while x < len(upPrices):
			if x <15:
				avg_gain.append(0)
				avg_loss.append(0)
			else:
				sumGain = 0
				sumLoss = 0
				y = x-14
				while y<=x:
					sumGain += upPrices[y]
					sumLoss += downPrices[y]
					y += 1
				avg_gain.append(sumGain/14)
				avg_loss.append(abs(sumLoss/14))
			x += 1
		p = 0
		RS = []
		RSI = []
		#  Loop to calculate RSI and RS
		while p < len(avg_closing_price):
			if p <15:
				RS.append(0)
				RSI.append(0)
			else:
				RSvalue = (avg_gain[p]/avg_loss[p])
				RS.append(RSvalue)
				RSI.append(100 - (100/(1+RSvalue)))
			p+=1
		j += 1
	print(avg_closing_price)
	print(RSI)	

main()
	# Wait for 1 second, to avoid API limit
	# time.sleep(1)
	# print(len(b))

# compute SMA & EMA based on currentPrice
	# we can probably find equations online 

# compute RSI = 100 - (100/(1+RS))
# RS = Relative Strength = AvgU / AvgD
# AvgU = average of all up moves in the last N price bars
# AvgD = average of all down moves in the last N price bars
# N = the period of RSI
# There are 3 different commonly used methods for the exact calculation of AvgU and AvgD (see details below)



# calculate 


# getData(checkPrice,currency)