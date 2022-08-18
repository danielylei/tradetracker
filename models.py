# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

class Tag(models.Model):
    name = models.CharField(max_length=20)

    class Meta: 
        ordering = ['name']

    def __str__(self):
        return self.name

class Trade(models.Model):
    date = models.DateTimeField('date traded')
    symbol = models.CharField(max_length=10)
    volume = models.IntegerField(default=1)
    pnl = models.FloatField()
    tags = models.ManyToManyField(Tag)
    #fee = models.FloatField()
    #commissions = models.FloatField()

    class Meta:
        ordering = ['date', 'symbol']

class Execution(models.Model):
    description = models.CharField(max_length=100)
    quantity = models.IntegerField(default=1)
    price = models.FloatField()
    amount = models.FloatField()
    commission = models.FloatField()
    fees = models.FloatField()
    payment_type = models.CharField(max_length=20)
    trade = models.ForeignKey(Trade, on_delete=models.CASCADE)





