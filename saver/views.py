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
def shares_saver(api,api_result):
    # api_result = JSON result from api for all market
    # pass api so we could call the api with get_share method to save market and industry in db
    
    # TODO: We are calling the api with get_all_now method and in that we dont get market type (bourse,farabourse) and state of shares but if we call with get_share
    # we would get that data and save it, we should everytime we want to save a share call api with get_share method and save those info 
    # -------------------- Completed ------------------------
    # posibile problem: maybe we reach our api limits 
    
    for x in api_result:
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
        # calling api is limitted for now i just commented this. when we improve our api we should uncomment the code below        
        # res = api.get_share(s.name)
        # s.market = res['market']
        # s.industry = res['type']
        # s.state = res['state']
        s.save()


def saver(request):
    token = '8e58c3d3ab6d07b04d21ae2f7b9b1252'
    api = SourceArena(token)
    res = api.get_all_now(0)
    shares_saver(api,res)
    html = "<html><body>Data saved to db</body></html>"
    return HttpResponse(html)