import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt 

def computeRSI(price_data,N = 14):
	'''
	RSI - relative strength index: momentum oscillator that predicts oversold/overbough conditions
	
	N - window of closing price (default is 14)
	price_data - array with closing price data

	'''

	
	
