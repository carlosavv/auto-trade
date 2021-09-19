#!/usr/bin/env python3
import cbpro 
import time 
import sys
from holoviews import streams
import streamz
import streamz.dataframe
from holoviews.streams import Pipe, Buffer 
import pandas as pd


class WSclient(cbpro.WebsocketClient):
	def __init__(self, datastream, **kwargs):
		super().__init__(**kwargs)
		self.datastream = datastream
		self.set_update_function()
	
	def get_datastream_type(self):
		return type(self.datastream)

	def set_update_function(self):
		
		if isinstance(self.datastream, Buffer):
			self.updater = self.update_buffer
		
		elif isinstance(self.datastream, streamz.dataframe.DataFrame):
			self.updater = self.update_stream_df
		
		elif isinstance(self.datastream, streamz.core.Stream):
			self.updater = self.update_dic

		elif isinstance(self.datastream, dict):
			self.updater = self.update_dic
		else:
			print('Error: Unsupported datastream type')
			self.updater = self.update_print
	def update_buffer(self, **kwargs):
		price_val = kwargs.get('price')
		time_val  = kwargs.get('time')
		
		self.datastream.send(pd.DataFrame({       # .send() works for Buffer objects
				'timestamp':[time_val],
				'price'    :[price_val],
			}).set_index('timestamp'))

	def update_stream_df(self, **kwargs):
		price_val = kwargs.get('price')
		time_val  = kwargs.get('time')
		
		self.datastream.emit(pd.DataFrame({       # .emit() is for Stream objects
				'timestamp':[time_val],
				'price'    :[price_val]
			}).set_index('timestamp'))
		
	def update_dic(self, **kwargs):
		self.datastream['time'].append(kwargs.get('time'))
		self.datastream['time'].append(kwargs.get('price'))
	
	def update_print(self,**kwargs):
		price_val = kwargs.get('price',None)
		time_val  = kwargs.get('time',None)
		print(f"DUDE {time_val} {price_val}")

	def on_open(self):
		self.url = "wss://ws-feed-public.sandbox.pro.coinbase.com"
		self.message_counter = 0

	def on_message(self,msg):
		self.message_counter += 1
		msg_type = msg.get('type')
		if msg_type == 'ticker':
			time = msg.get('time')
			time = pd.Timestamp(time)
			price = float(msg.get('price'))
			print(time,price)
			self.updater(price = price, time = time)
	
	def on_close(self):
		print(f"<---Websocket connection closed--->\n\tTotal messages: {self.message_counter}")

class GraphicWebsocketClient(WSclient):
	def explanation(self):
		print('This class is created to maintain backwards compatibility with my previous scripts')
		print('However, the name GraphicWebsocketClient does really make sense, so I changed the official')
		print('name of the class to CBWebsocketClient and created this child since I was too lazy to fix my code.')
