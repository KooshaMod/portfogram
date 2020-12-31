from django.db import models

# Create your models here.
class DataSymbol(models.Model):
    def __str__(self):
        msg = "Price of {} is {} at {}"
        return msg.format(self.symbol,
                          self.price,
                          self.date)
    symbol = models.CharField(max_length=20)
    price = models.IntegerField()
    date = models.DateTimeField()

    @classmethod
    def check_exist(cls, symbol, date):
        return cls.objects.filter(symbol=symbol).filter(date=date).count() > 0

    @classmethod
    def read_last(cls, symbol):
        if DataSymbol.objects.count() > 0:
            # TODO (hadi): avoid getting the full list
            # getting last row with last method
            return cls.objects.filter(symbol=symbol).last()
        else:
            return None


class DataShare(models.Model):
    def __str__(self):
        return "Share {} data. with id {}".format(self.name,self.id)

    name = models.CharField(max_length=50)
    full_name = models.TextField()
    first_price = models.IntegerField()
    yesterday_price = models.IntegerField()
    close_price = models.IntegerField()
    close_price_change_percent = models.FloatField()
    final_price = models.IntegerField()
    final_price_change_percent = models.FloatField()
    eps = models.IntegerField()
    highest_price = models.IntegerField()
    lowest_price = models.IntegerField()
    pe = models.FloatField()
    trade_volume = models.BigIntegerField()
    trade_value = models.BigIntegerField()
    market_value = models.BigIntegerField()
    date = models.DateTimeField()
    #new data from api need to remigrate model
    industry = models.TextField()
    market = models.TextField()
    state = models.TextField()




