from django.db import models

class ItemType(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.name
    
class Vendor(models.Model):
    name = models.CharField(max_length=50)
    phoneNumber = models.CharField(max_length=50,default='0')

    def __str__(self) -> str:
        return self.name

class Item(models.Model):
    name = models.CharField(max_length=50)
    itemType = models.ForeignKey(ItemType,on_delete=models.CASCADE)
    quantity = models.FloatField()
    requiredPurchaseQuantity = models.FloatField(default=0.0)
    quantityType = models.CharField(max_length=50, choices=(('Kg','Kg'),('Unit','Unit'),('Box','Box')))
    isExpirable = models.BooleanField(default=False)
    vendor = models.ForeignKey(Vendor,on_delete=models.CASCADE,null=True,blank=True)

    def __str__(self) -> str:
        return self.name



class PurchaseItem(models.Model):
    item = models.ForeignKey(Item,on_delete=models.CASCADE)
    quantity = models.FloatField()
    quantityType = models.CharField(max_length=50, choices=(('Kg','Kg'),('Unit','Unit'),('Box','Box')))
    pricePerItem = models.FloatField()
    totalPrice = models.FloatField()
    expiryDate = models.DateField(blank=True,null=True)

    def __str__(self) -> str:
        return self.item.name + ' - ' + str(self.quantity) 

class Purchase(models.Model):
    purchaseItems = models.ManyToManyField(PurchaseItem)
    totalPrice = models.FloatField()
    dateTime = models.DateTimeField(auto_now_add=True)
    vendor = models.ForeignKey(Vendor,on_delete=models.CASCADE)
    isFullyPaid = models.BooleanField(default=True)
    remarks = models.CharField(max_length=250)
    def __str__(self) -> str:
        return str(self.dateTime)

class Wastage(models.Model):
    item = models.ForeignKey(Item,on_delete=models.CASCADE)
    quantity = models.FloatField()
    quantityType = models.CharField(max_length=50, choices=(('Kg','Kg'),('Unit','Unit'),('Box','Box')))
    wastageType = models.CharField(max_length=50, choices=(('Expired','Expired'),('Spoiled','Spoiled'),('Own usage','Own usage'),('Missing','Missing'),('Other','Other')))
    dateTime = models.DateTimeField(auto_now_add=True)

class ItemToPurchase(models.Model):
    item = models.ForeignKey(Item,on_delete=models.CASCADE)
    requirmentPostedOn = models.DateTimeField(auto_now_add=True)
    requirmentpurchasedOn = models.DateTimeField(null=True,blank=True)
    remarks = models.CharField(max_length=250)
    purchased = models.BooleanField(default=False)

    

class DailyInventoryCheck(models.Model):
    itemsToPurchase = models.ManyToManyField(ItemToPurchase)
    totalRequiredItems = models.IntegerField()
    dateTime = models.DateTimeField(auto_now_add=True)
    isFullyCompleted = models.BooleanField(default=False)

    def __str__(self) -> str:
        return str(self.dateTime)