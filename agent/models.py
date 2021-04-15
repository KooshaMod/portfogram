from django.db import models

# Create your models here.
class Candle:
	def __repr__(self):
		return f"candle of {self.date} with close price of {self.close_price}"

	def __init__(self,date,close_price=None,final_price=None,first_price=None,highest_price=None,lowest_price=None,trade_volume=None,trade_number=None,trade_value=None):
		self.date = date
		self.close_price = close_price
		self.final_price = final_price
		self.first_price = first_price
		self.highest_price = highest_price
		self.lowest_price = lowest_price
		self.trade_value = trade_value
		self.trade_volume = trade_volume
		self.trade_number = trade_number

	def __eq__(self,other):
		if isinstance(other, Candle):
			return self.date == other.date
		return False

class Chart:
	def __init__(name,chandles):
		self.share_name = name
		self.candles = candles
