import cbpro
import pandas as pd
import time 
import datetime as dt
import numpy as np
from tools_test import get_CurrentPrice

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
	period = 300
	auth_client = cbpro.AuthenticatedClient(key,secret,passphrase)
	# Get the currency's specific ID
	# specificID = get_SpecificAccount(auth_client,currency[:3])
	# currentPrice = []
	while checkPrice == True:
		currentPrice,price_mat = get_CurrentPrice(auth_client,currency,period)
		time.sleep(1)
		print(price_mat)
		
	
		
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