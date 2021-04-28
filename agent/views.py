from django.shortcuts import render
from stocks.models import DataShare
from saver.models import SourceArena
from agent.models import Candle
import matplotlib.pyplot as plt
#marketdata return all the shares in a list
from filter.views import market_data
import numpy as np
import pandas as pd
import jdatetime
import pdb


def to_int(s):
	if s:
		return int(s)
	return 0

def to_float(s):
	if s:
		return float(s)
	return 0

def make_data_same_len(candles_dict,CONFIG):
	'''
	get a dictionary with the key of shares name and list of candles as value
	make all the values became same size(fill the missing date's data)
	return the dictonary of candles_dict
	'''

	dates = [x.date for x in candles_dict[CONFIG.get('share_name')]]

	for share in candles_dict.keys():

		missing_dates = [x for x in dates if x not in [y.date for y in candles_dict[share]]]
		# getting rid of extra data
		can_list = []
		for i in range(0,len(candles_dict[share])):
			if candles_dict[share][i].date in dates:
				can_list.append(candles_dict[share][i])

		candles_dict[share] = can_list 
		# adding missing data with none value
		for d in missing_dates:
			candles_dict[share].append(Candle(d))

		# removing duplicated data
		for can in candles_dict[share]:
			if candles_dict[share].count(can) > 1:
				candles_dict[share].remove(can)

		candles_dict[share].sort(key = lambda x : x.date,reverse=True)

	return candles_dict


# Create your views here.
def agent_ren(request):
	CONFIG= {'share_name' : request.GET.get('share_name','')}
	CONFIG['days'] = to_int(request.GET.get('days',''))
	CONFIG['accepted_cor'] = to_float(request.GET.get('accepted_cor',''))
	CONFIG['accepted_diff'] = to_float(request.GET.get('difference',''))
	print(CONFIG)
	file = open('../token.txt','r')
	token = file.read()
	file.close()
	api = SourceArena(token)
	if CONFIG['share_name'] and CONFIG['days']:
		share_industry = DataShare.objects.filter(name=CONFIG['share_name']).last().industry
		market_shares = market_data()
		shares_name_in_ind = [share.name for share in market_shares if share.industry == share_industry]
		shares_name_in_ind.append(CONFIG['share_name'])
		candles_dict = {}
		for share in shares_name_in_ind:
			res = api.get_recent_days(share,CONFIG['days'])
			candles_list = []
			for can in res:
				candles_list.append(Candle(jdatetime.date(
											int(can.get('date')[:4]),
											int(can.get('date')[5:7]),
											int(can.get('date')[8:])
											)
											,to_int(can.get('close_price')),
											to_int(can.get('final_price')),to_int(can.get('first_price')),
											to_int(can.get('highest_price')),to_int(can.get('lowest_price')),
											to_int(can.get('trade_volume')),to_int(can.get('trade_number')),
											to_int(can.get('trade_value'))))
			candles_dict[share] = candles_list

		candles_dict = make_data_same_len(candles_dict,CONFIG)
		dates = [can.date for can in candles_dict[CONFIG['share_name']]]
		closed_price_dict = {k:[v.close_price for v in values] for (k,values) in candles_dict.items()}
		df = pd.DataFrame.from_dict(closed_price_dict)
		df['date'] = dates
		df.set_index('date',inplace=True)
		df_cor = df.corr()
		high_cor = [x for x in df_cor[df_cor[CONFIG['share_name']]>CONFIG.get('accepted_cor')].index]
		averages = {k:df[k].mean() for k in high_cor}
		result = []
		for key in high_cor:
			if abs(df.iloc[0][CONFIG['share_name']]/averages[CONFIG['share_name']] - df.iloc[0][key]/averages[key]) > CONFIG.get('accepted_diff'):
				result.append(key)
		print('------res----------')
		print(result)

		return render(request,'agent.html',{'res':result})
	else:
		return render(request,'agent.html')



