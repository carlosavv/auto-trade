import cbpro
import pandas as pd
import time 
import datetime as dt
import numpy as np
import glob,os

def getSpecificAccount(cur):
    x = auth_client.get_accounts()
    for account in x:
        if account['currency'] == cur:
            return account['id']

def get_currencyPrice(auth_client,currency):

	# Get the currency's specific ID
	specificID = getSpecificAccount(currency[:3])
	# Granularity (in seconds). So 300 = data from every 5 min (300s/60s = 5 mins)
	period = 300
	# We will keep track of how many iterations our bot has done
	iterations = 0

	while iterations < 10:

		try:

			historicData = auth_client.get_product_historic_rates(currency, granularity=period)

	    	# Make an array of the historic price data from the matrix
			price = np.squeeze(np.asarray(np.matrix(historicData)[:,4]))

	    	# Wait for 1 second, to avoid API limit
			time.sleep(1)

			# Get latest data and show to the user for reference
			newData = auth_client.get_product_ticker(product_id=currency)
			# print(newData)
			currentPrice=newData['price']
			# print(str(currency) + " price =",currentPrice)
			iterations += 1
			# print(iterations)
			return currentPrice

		except:
			print('error')

path = str(input("Enter the directory where your API Keys are: "))
df = pd.read_csv(path)
keys = df.columns.values
key = keys[0]
secret = keys[1]
passphrase = keys[2]
checkPrice = True
currency = 'BTC-USD'

pub_client = cbpro.PublicClient()
auth_client = cbpro.AuthenticatedClient(key,secret,passphrase)
get_currencyPrice(auth_client,currency)


# compute SMA & EMA based on currentPrice
	# we can probably find equations online 

# compute RSI = 100 - (100/(1+RS))
# RS = Relative Strength = AvgU / AvgD
# AvgU = average of all up moves in the last N price bars
# AvgD = average of all down moves in the last N price bars
# N = the period of RSI
# There are 3 different commonly used methods for the exact calculation of AvgU and AvgD (see details below)


# def RSIfun(price, n=14):
#     delta = price['Close'].diff()
#     #-----------
#     dUp=
#     dDown=

#     RolUp=pd.rolling_mean(dUp, n)
#     RolDown=pd.rolling_mean(dDown, n).abs()

#     RS = RolUp / RolDown
#     rsi= 100.0 - (100.0 / (1.0 + RS))
	# dUp= delta[delta > 0]
	# dDown= delta[delta < 0]

	# dUp = dUp.reindex_like(delta, fill_value=0)
	# dDown = dDown.reindex_like(delta, fill_value=0)

	# dUp, dDown = delta.copy(), delta.copy()
	# dUp[dUp < 0] = 0
	# dDown[dDown > 0] = 0

	# RolUp = pd.rolling_mean(dUp, n)
	# RolDown = pd.rolling_mean(dDown, n).abs()

	# RS = RolUp / RolDown

#     return rsi

# calculate 


# getData(checkPrice,currency)
