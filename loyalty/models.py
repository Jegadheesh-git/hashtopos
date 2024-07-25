from django.db import models
from menu.models import MenuItem

# Create your models here.
class Customer(models.Model):
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    phone = models.CharField(max_length=10, primary_key=True)
    loyaltyPoints = models.FloatField()

    def __str__(self) -> str:
        return self.name + " " + self.phone


class Coupons(models.Model):
    name = models.CharField(max_length=50)
    flatDiscountAmount = models.FloatField(default=0)
    discountPercentage = models.FloatField(default=0)
    loyaltyPoints = models.FloatField(default=0)
    maximumBillValue = models.FloatField(default=0)
    couponType = models.CharField(max_length=30,choices=(('Flat','Flat'),('Percentage','Percentage'),('Loyalty','Loyalty')))
    hasCouponApplied = models.BooleanField(default=False)
    items = models.ManyToManyField(MenuItem)
    createdAt = models.DateTimeField(auto_now_add=True)
    validFrom = models.DateTimeField()
    validTill = models.DateTimeField()

    def __str__(self) -> str:
        return self.name + ' from '+ str(self.validFrom) +' to '+ str(self.validTill)
    
class CustomerFeedback(models.Model):
    dateTime = models.DateTimeField(auto_now_add=True)
    customerName = models.CharField(max_length=50,blank=True,null=True)
    feedBackType = models.CharField(max_length=50,choices=(('Good review','Good review'),('Taste Issue','Taste Issue'),('Order Delay','Order Delay'),('Item Unavailable','Item Unavailable'),('Item Add suggestion','Item Add Suggestion'),('Other','Other')))
    feedbackSummary = models.CharField(max_length=250)
    reasonForIssue = models.CharField(max_length=250,blank=True,null=True)
    hasDiscussed = models.BooleanField(default=False)
    closureSummary = models.CharField(max_length=250)

    def __str__(self) -> str:
        return self.feedBackType + ' - '+ str(self.dateTime)