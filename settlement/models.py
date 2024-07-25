from django.db import models
from billing.models import *
from datetime import datetime
# Create your models here.
class SettlementPercentage(models.Model):
    sharePercentage = models.FloatField()

    def __str__(self) -> str:
        return str(self.sharePercentage)

class Settlement(models.Model):
    dateTime = models.DateTimeField(auto_now_add=True)
    bills = models.ManyToManyField(Bill)
    totalSaleAmount = models.FloatField()
    totalParcelAmount = models.FloatField()
    totalPastBalanceAmount = models.FloatField()
    totalAmountToBeSettled = models.FloatField()
    paymentRecieved = models.FloatField()
    balancePayment = models.FloatField()
    paymentFrom = models.CharField(max_length=30,default="Shri Fresh 2 Fresh")
    paymentTo = models.CharField(max_length=30,default="Hashtopia Foods")
    payerCollectedAmount = models.FloatField()
    isFullyPaid = models.BooleanField(default=False)
    balanceAmountCarryForwardedOn  = models.DateTimeField(null=True,blank=True)

    def __str__(self) -> str:
        return str(self.dateTime)+' '+str(self.paymentRecieved)

class DailyReport(models.Model):
    dateTime = models.DateTimeField(auto_now_add=True)
    totalCollection = models.FloatField()
    totalSale = models.FloatField()
    totalParcel = models.FloatField()
    totalOrders = models.FloatField()
    hfShare = models.FloatField()
    ftfShare = models.FloatField()
    hfTotalAmount = models.FloatField()
    hfTotalExpense = models.FloatField()
    hfTotalPurchase = models.FloatField()
    summary = models.CharField(max_length=250)

    def __str__(self) -> str:
        return str(self.dateTime)+ " - "+str(self.totalCollection)

    