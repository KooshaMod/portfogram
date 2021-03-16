from django.shortcuts import render
from stocks.models import DataShare
from statistics import mean


def market_data():
	'''
	return a list of all shares of market
	'''
	#TODO: find a better way to do this querry.
	all_shares = list(DataShare.objects.all())[::-1]
	shares_name = []
	result = []
	for share in all_shares:
		if share.name not in shares_name:
			shares_name.append(share.name)
			result.append(share)
	return result


def pe(share):
	return float(DataShare.objects.filter(name=share).last().pe)


def avg(iter_obj):
	return mean(iter_obj)


def trade_value(share,days=1):
	shares = list(DataShare.objects.filter(name=share))[::-1]
	if days == 1: 
		return int(shares[0].trade_value)
	res = []
	last_date_saved = shares[0].date.date()
	res.append(shares[0].trade_value)
	for share in shares:
		if len(res)<days:
			if last_date_saved != share.date.date():
				res.append(share.trade_value)
				last_date_saved = share.date.date()
		else:
			break
	return res


def trade_volume(share,days=1):
	shares = list(DataShare.objects.filter(name=share))[::-1]
	if days == 1: 
		return int(shares[0].trade_volume)
	res = []
	last_date_saved = shares[0].date.date()
	res.append(shares[0].trade_volume)
	for share in shares:
		if len(res)<days:
			if last_date_saved != share.date.date():
				res.append(share.trade_volume)
				last_date_saved = share.date.date()
		else:
			break
	return res

def market_size(share):
	return int(DataShare.objects.filter(name=share).last().market_value)

def fix_trade_vol(s):
	s = ''.join(s.split(' '))
	new_str = ""
	while True:
		x = s.find("trade_volume")
		if x == -1:
			new_str += s
			break
		new_str += s[:x+12]
		s = s[x+12:]
		sym = s[0:1]
		if sym != "(":
			new_str += "(x.name)"
		else:
			new_str += "(x.name,"
			s = s[1:]
	return new_str		

def fix_trade_values(s):
	s = ''.join(s.split(' '))
	new_str = ""

	while True:
		x = s.find("trade_value")
		if x == -1:
			new_str += s
			break
		new_str += s[:x+11]
		s = s[x+11:]
		sym = s[0:1]
		if sym != "(":
			new_str += "(x.name)"
		else:
			new_str += "(x.name,"
			s = s[1:]
	return new_str		

def add_param(s):
	'''
	changing the input string to a readable code by python
	'''
	s = s.replace('pe','pe(x.name)')
	s = s.replace('market_size','market_size(x.name)')
	s = s.replace('trade_market','trade_market(x.name)')
	s = s.replace('=','==')
	s = s.replace('industry' , 'industry(x.name)')
	s = s.replace('sub_ind','sub_industry(x.name)')
	s = s.replace('is_sell_queue','is_sell_queue(x.name)')
	s = s.replace('is_buy_queue','is_buy_queue(x.name)')
	s = s.replace('demand_vol','demand_vol(x.name)')
	s = s.replace('supply.vol','supply_vol(x.name)')
	s = s.replace('buy_count','buy_count(x.name)')
	s = s.replace('sell_count','sell_count(x.name)')
	s = s.replace('basis_volume','basis_volume(x.name)')
	s = s.replace('all_stocks', 'all_stocks(x.name)')
	s = s.replace('close_price','close_price(x.name)')
	s = s.replace('final_price','final_price(x.name)')
	#trade value
	s = fix_trade_values(s)
	#trade volume
	s = fix_trade_vol(s)
	s = s.replace('and',' and ')
	s = s.replace('or', ' or ')
	s = s.replace('&', ' and ')
	s = s.replace('|', ' or ')
	#add '' to fixed input	
	s = s.replace('بورس', '"بورس"')
	s = s.replace('فرابورس','"فرابورس"')

	#sub_industries and industry
	shares = market_data()
	sub_industries = []
	industries = []
	for share in shares:
		if share.industry not in industries:
			industries.append(share.industry)
		if share.sub_industry not in sub_industries:
			sub_industries.append(share.sub_industry)
	for sub_i in sub_industries:
		replacement = '"'+sub_i+'"'
		if s.find(sub_i) != -1 and sub_i:
			s = s.replace(sub_i,replacement)
	for ind in industries:
		replacement = '"'+ind+'"'
		if s.find(ind) != -1 and ind:
			s = s.replace(ind,replacement)
	return s


def demand_vol(share):
	share = DataShare.objects.filter(name=share).last()
	return share.first_row_buy_vol + share.sec_row_buy_vol + share.third_row_buy_vol


def supply_vol(share):
	share = DataShare.objects.filter(name=share).last()
	return share.first_row_sell_vol + share.sec_row_sell_vol + share.third_row_sell_vol


def industry(share):
	return DataShare.objects.filter(name=share).last().industry


def sub_industry(share):
	return DataShare.objects.filter(name=share).last().sub_industry


def trade_market(share):
	return DataShare.objects.filter(name=share).last().market


def is_sell_queue(share):
	share = DataShare.objects.filter(name=share).last()
	if share.daily_price_low == share.first_row_sell_price and share.first_row_buy_vol==0:
		return True
	return False


def is_buy_queue(share):
	share = DataShare.objects.filter(name=share).last()	
	if share.daily_price_high == share.first_row_buy_price and share.first_row_sell_vol==0:
		return True
	return False


def buy_count(share):
	share = DataShare.objects.filter(name=share).last()
	return share.first_row_buy_count + share.sec_row_buy_count + share.third_row_buy_count


def sell_count(share):
	share = DataShare.objects.filter(name=share).last()
	return share.first_row_sell_count + share.sec_row_sell_count + share.third_row_sell_count


def basis_volume(share):
	return DataShare.objects.filter(name=share).last().basis_vol


def all_stocks(share):
	return DataShare.objects.filter(name=share).last().all_stocks


def final_price(share):
	return DataShare.objects.filter(name=share).last().final_price


def close_price(share):
	return DataShare.objects.filter(name=share).last().close_price


def filter(request):
	'''
	accept a request and call add_param function to make it python readable and run the expression in every shares and filter them
	'''
	res = request.GET.get('entered_filter','')
	result = []

	if res:
		res = add_param(res)
		print(f'string after parsing is \n {res}')
		shares = market_data()
		for x in shares:
			if eval(res):
				result.append(x.name)
	a = DataShare.objects.filter(name='هجرت').last()
	print(f"هجرت final = {a.final_price} and close = {a.close_price}")	
	return render(request,'filter.html',{'res':result})




