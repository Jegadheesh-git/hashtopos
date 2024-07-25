from django.db import models
from menu.models import MenuItem
from loyalty.models import Coupons
from django.contrib.auth.models import User

# Create your models here.
class OrderItem(models.Model):
    menuItem = models.ForeignKey(MenuItem,on_delete=models.CASCADE)
    quantity = models.IntegerField()
    totalPrice = models.FloatField()
    finalPrice = models.FloatField()
    isParcel = models.BooleanField(default=False)
    parcelQuantity = models.IntegerField(default=0)
    parcelCharge = models.FloatField(default=0.0)

    def __str__(self) -> str:
        return self.menuItem.name +' - '+str(self.quantity)+'- '+str(self.totalPrice)
    
class OrderMode(models.Model):
    name = models.CharField(max_length=50)
    colour = models.CharField(max_length=50)
    quickBill = models.BooleanField(default=False)
    def __str__(self)->str:
        return self.name

class OrderStatus(models.Model):
    name = models.CharField(max_length=50)
    colour = models.CharField(max_length=50)

    def __str__(self)->str:
        return self.name

class Order(models.Model):
    orderItems = models.ManyToManyField(OrderItem)
    totalPrice = models.FloatField()
    finalPrice = models.FloatField()
    totalParcelCharge = models.FloatField(default=0.0)
    finalPriceIncludedParcel = models.FloatField(default=0.0)
    orderDateTime = models.DateTimeField(auto_now_add=True)
    orderDeliveredDateTime = models.DateTimeField(blank=True,null=True)
    totalTimeTakenForPreparation = models.DurationField(blank=True, null=True)
    orderStatus = models.ForeignKey(OrderStatus,on_delete=models.CASCADE)
    orderMode = models.ForeignKey(OrderMode,on_delete=models.CASCADE)
    takenBy = models.ForeignKey(User,on_delete=models.CASCADE)
    couponUsed = models.ForeignKey(Coupons,on_delete=models.CASCADE,null=True, blank=True)
    hasCouponApplied = models.BooleanField(default=False)
    note = models.CharField(max_length=50,null=True,blank=True)
    

    def __str__(self) -> str:
        return str(self.pk)+' '+str(self.orderDateTime)