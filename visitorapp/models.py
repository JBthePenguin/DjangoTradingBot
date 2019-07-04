from django.db import models


class Binance(models.Model):
    """Model with api's keys, cryptocurrencies and markets"""
    api_key = models.CharField(max_length=65)
    secret_key = models.CharField(max_length=65)
    currency_one = models.CharField(max_length=3)
    currency_two = models.CharField(max_length=3)
    currency_three = models.CharField(max_length=3)
    market_one = models.CharField(max_length=6)
    market_two = models.CharField(max_length=6)
    market_three = models.CharField(max_length=6)
