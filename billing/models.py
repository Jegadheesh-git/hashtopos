from django.db import models
from menu.models import MenuItem
from loyalty.models import Customer, Coupons
from django.contrib.auth.models import User
from order.models import Order
# Create your models here.


class Bill(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, blank=True, null=True)
    dateTime = models.DateTimeField(auto_now_add=True)
    billedBy = models.ForeignKey(User,on_delete=models.CASCADE)
    settlementStatus = models.BooleanField(default=False)
    modeOfPayment = models.CharField(max_length=50,choices=(('Cash','Cash'),('UPI','UPI'),('Bank Transfer','Bank Transfer')))
