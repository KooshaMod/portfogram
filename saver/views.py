from django.shortcuts import render, HttpResponse
from stocks.models import DataShare
from django.utils import timezone
import requests
# Create your views here.

def to_float(s):
    if isinstance(s, (float, int)):
        return s
    elif isinstance(s, str):
        return float(''.join(s.split(',')))
    msg = "{} has type {} which is not a supported format."
    raise ValueError(msg.format(s, type(s)))


def to_int(s):
    if isinstance(s, int):
        return s
    elif isinstance(s, str):
        return round(to_float(s))
    elif s == None:
        return 0
    msg = "{} has type {} which is not a supported format."
    raise ValueError(msg.format(s, type(s)))


class SourceArena:
    def __init__(self, token):
        self.base_url = 'https://sourcearena.ir/api'
        self.token = token

    def get_currencies(self):
        params = {'token':self.token, 'currency':''}
        response = requests.get(self.base_url, params=params)
        return response.json()

    def get_market(self, market, time):
        params = {'token':self.token, 'market':market, 'time':time }
        response = requests.get(self.base_url, params=params)
        return response.json()

    def get_market_growth(self, time_a, time_b, market='market_bourse'):
        market1 = self.get_market(market, time_a)
        index1 = to_int(market1['bourse']['index'])
        market2 = self.get_market(market, time_b)
        index2 = to_int(market2['bourse']['index'])
        return index2/index1
    # TODO: Check if we can have 2 method with same name with different parameters (polymorphism) in python
    def get_share_by_time(self,name,time):
        params = {'token':self.token, 'name':name,'time':time}
        response = requests.get(self.base_url, params=params)
        return response.json()
    def get_share(self,name):
        params = {'token':self.token, 'name':name}
        response = requests.get(self.base_url, params=params)
        return response.json()


    def get_all_now(self,type=2):
        '''
        type = 0 > only bourse and farabourse
        type = 1 > only hagh taghadom and sandogh
        type = 2 > all
        '''
        params = {'token':self.token, 'all':'all', 'type': type}
        response = requests.get(self.base_url, params=params)
        return response.json()


def shares_saver(api):
    
    res = api.get_all_now(0)
    count = 0
    for x in res:
        print(count)
        count += 1
        s = DataShare()
        s.name = x['name']
        s.full_name = x['full_name']
        s.first_price = to_int(x['first_price'])
        s.yesterday_price = to_int(x['yesterday_price'])
        s.close_price = to_int(x['close_price'])
        s.close_price_change_percent = float(
            x['close_price_change_percent'][:-1])
        s.final_price = to_int(x['final_price'])
        s.final_price_change_percent = float(
            x['final_price_change_percent'][:-1])
        if x['eps'] == '':
            s.eps = 0
        else:
            s.eps = to_int(x['eps'])
        s.highest_price = to_int(x['highest_price'])
        s.lowest_price = to_int(x['lowest_price'])
        s.pe = to_float(x['P:E'])
        s.trade_volume = to_int(x['trade_volume'])
        s.trade_value = to_int(x['trade_value'])
        s.market_value = to_int(x['market_value'])
        s.date = timezone.now()
        s.market = x['market']
        s.state = x['state']
        s.daily_price_high = to_int(x['daily_price_high'])
        s.daily_price_low = to_int(x['daily_price_low'])
        s.trade_num = to_int(x['trade_number'])
        s.all_stocks = to_int(x['all_stocks'])
        s.basic_vol = to_int(x['basis_volume'])
        s.read_buy_vol = to_int(x['real_buy_volume'])
        s.co_buy_vol = to_int(x['co_buy_volume'])
        s.read_sell_vol = to_int(x['real_sell_volume'])
        s.co_sell_vol = to_int(x['co_sell_volume'])
        s.real_buy_count = to_int(x['real_buy_count'])
        s.co_buy_count = to_int(x['co_buy_count'])
        s.real_sell_count = to_int(x['real_sell_count'])
        s.co_sell_count = to_int(x['co_sell_count'])

        s.first_row_sell_count = to_int(x['1_sell_count'])
        s.sec_row_sell_count = to_int(x['2_sell_count'])
        s.third_row_sell_count = to_int(x['3_sell_count'])
        s.first_row_buy_count = to_int(x['1_buy_count'])
        s.sec_row_buy_count = to_int(x['2_buy_count'])
        s.third_row_buy_count = to_int(x['3_buy_count'])
        s.first_row_sell_price = to_int(x['1_sell_price'])
        s.sec_row_sell_price = to_int(x['2_sell_price'])
        s.third_row_sell_price = to_int(x['3_sell_price'])
        s.first_row_buy_price = to_int(x['1_buy_price'])
        s.sec_row_buy_price = to_int(x['2_buy_price'])
        s.third_row_buy_price = to_int(x['3_buy_price'])
        s.first_row_sell_vol = to_int(x['1_sell_volume'])
        s.sec_row_sell_vol = to_int(x['2_sell_volume'])
        s.third_row_sell_vol = to_int(x['3_sell_volume'])
        s.first_row_buy_vol = to_int(x['1_buy_volume'])
        s.sec_row_buy_vol = to_int(x['2_buy_volume'])
        s.third_row_buy_vol = to_int(x['3_buy_volume'])
        # some data from another method of api       
        res = api.get_share(s.name)
        s.industry = res['type']
        s.sub_industry = res['sub_type']
        s.save()


def saver(request):
    token = '8e58c3d3ab6d07b04d21ae2f7b9b1252'
    api = SourceArena(token)
    shares_saver(api)
    # res = api.get_all_now(0)
    # html = f"<html><body>{res}</body></html>"
    # DataShare.objects.all().delete()
    html = "<html><body >saved to db</body></html>"

    return HttpResponse(html)