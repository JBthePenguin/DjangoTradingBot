from django.db import models
from django.utils import timezone


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
    quantity_bnb = models.IntegerField(default=1)
    start_date = models.DateField(default=timezone.now)


class Market(models.Model):
    symbol = models.CharField(max_length=6)
    position = models.IntegerField(db_index=True, default=0)


class Order(models.Model):
    market = models.ForeignKey(Market, on_delete=models.CASCADE)
    side = models.CharField(max_length=4)
    quantity = models.CharField(max_length=20)
    price = models.CharField(max_length=20)
    is_completed = models.BooleanField(default=False)


class Trade(models.Model):
    open_date = models.DateTimeField(db_index=True, auto_now_add=True)
    closed_date = models.DateTimeField(null=True, default=None)
    order_one = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="trade_order_one")
    order_two = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="trade_order_two")
    order_three = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="trade_order_three")
    is_completed = models.BooleanField(db_index=True, default=False)
    fee = models.FloatField(default=0)


class Error(models.Model):
    date = models.DateTimeField(db_index=True, auto_now_add=True)
    type_error = models.CharField(max_length=60)


class Offset(models.Model):
    trade_number = models.IntegerField()
    bnb = models.FloatField()
