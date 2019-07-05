from django.db import models


class BinanceKey(models.Model):
    """Model with api's keys, cryptocurrencies and markets"""
    api = models.CharField(max_length=65)
    secret = models.CharField(max_length=65)


class Currency(models.Model):
    """ Model for crypto currency with name and symbol """
    name = models.CharField(max_length=20)
    symbol = models.CharField(max_length=3)
    position = models.IntegerField(db_index=True, default=0)


class Bank(models.Model):
    name = models.CharField(db_index=True, max_length=5)
    amount_currency_one = models.FloatField()
    amount_currency_two = models.FloatField()
    amount_currency_three = models.FloatField()


class Bot(models.Model):
    is_working = models.BooleanField(default=False)
