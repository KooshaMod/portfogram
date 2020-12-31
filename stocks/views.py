from django.shortcuts import render
import requests
from .models import DataShare
from home.views import get_list_stocks
# from django.http import HttpResponse
# from json import dumps
from django.http import JsonResponse

import json
import jsonpickle
from json import JSONEncoder



def get_chart_info(name,days):
    #TODO: its better to write a class for candles with 4 high,low,open and close attributes. bc if we want to show chart with different timeframe we cant use these data from api and we should create it
    # but now that we only need daily chart we can use this
    stock_info = DataShare.objects.filter(name=name)
    # filter to save the last record in every day
    # stock_list is the final list that include the last data from each day
    stock_list = []
    # day and last_stock_inday are temporary variables to create stock_list
    day = stock_info[0].date.date()
    last_stock_inday = stock_info[0]
    # update the last last stock in the same day and when the day has been changed add that in stock_list
    # after iterating in stock_info we should add the last one bc we save to stock_list when the date has been changed and in the last date the date wont changes so we will not save that so we alwasy should save the last data in stock_list
    for x in stock_info:
        if x.date.date() == day:
            last_stock_inday = x
        else:
            stock_list.append(last_stock_inday)
            day = x.date.date()
            last_stock_inday = x
    # add the last index of stock_info in stock_list
    last_index = stock_info.count() - 1 
    stock_list.append(stock_info[last_index])

    if len(stock_list)<days:
        # if we dont have enough data we will make a list with days length and returning 0 beside missing record
        zero_list = [0] * (days - len(stock_list))
        stock_list = zero_list + stock_list
        return stock_list
    else:
        # the index that we need from that index to end
        index = len(stock_list)-days
        stock_list = stock_list[index:]
        return stock_list



def get_stock_data(stock_name):
    # return the last record of the given stock
    return DataShare.objects.filter(name=stock_name).last()



def stock(request):
    name = request.GET['stocks']
    stock = get_stock_data(name)
    chart_info = get_chart_info(name,2)
    # dataJson = dumps(chart_info)
    # this function imported from home.views to supliment the index.html with data for search list 
    stocks = get_list_stocks()
    # for x in chart_info:
    #     print("the id of record is {} and the last price is {}".format(x.id,x.last_price))
    # print(chart_info)
    # for x in chart_info:
    #     print("the id is {} and the price is {}".format(x.id,x.final_price))
    # print(chart_info[0].id)
    return render(request,'index.html',{'stock':stock, 'stocks' : stocks,})




def api(request):
    name = request.GET['name']
    chart_info = get_chart_info(name, 5)

    return JsonResponse(jsonpickle.encode(chart_info, unpicklable=False), safe=False)





  