from django.shortcuts import render
from stocks.models import DataShare
# Create your views here.
def get_list_stocks():
    # list of unique stocks
    return DataShare.objects.distinct('name')

def home(request):
    stocks = get_list_stocks()
    return render(request, 'home.html',{'stocks':stocks})