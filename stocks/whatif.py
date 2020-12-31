import os

from django.utils import timezone
from datetime import timedelta 

from .models import DataSymbol

def get_what_ifs():
    # Bourse looks like to be incorrect!
    symbols = ['USD', 'Ounce', 'Bitcoin', 'Bourse']
    convert_to_USD = [False, True, True, False]
    days = 14
    from_USD1 = DataSymbol.get_closest_to('USD', timezone.now()-timedelta(days=days)).price
    from_USD2 = DataSymbol.get_closest_to('USD', timezone.now()).price

    for symbol, need_convert in zip(symbols,convert_to_USD):  
        p1 = DataSymbol.get_closest_to(symbol, timezone.now()-timedelta(days=days)).price
        p2 = DataSymbol.get_closest_to(symbol, timezone.now()).price
        if need_convert:
            p1 = p1 * from_USD1
            p2 = p2 * from_USD2
        msg = "If {} days ago bought {} it was now {:4.4f}x more!"
        print(msg.format(days,symbol,p2/p1))
