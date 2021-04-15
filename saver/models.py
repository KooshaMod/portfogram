from django.db import models
import requests

# Create your models here.
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

    def get_recent_days(self,name,days):
    	params = {'token':self.token,'name':name,'days':days}
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
