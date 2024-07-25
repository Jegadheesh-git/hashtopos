from django.db import models
from inventory.models import Item

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self) -> str:
        return self.name
class SubCategory(models.Model):
    name = models.CharField(max_length=50)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.name

class MenuItem(models.Model):
    name = models.CharField(max_length=50)
    subCategory = models.ForeignKey(SubCategory,on_delete=models.CASCADE)
    price = models.FloatField()
    requiredRawMaterials = models.ManyToManyField(Item)
    isAvailable = models.BooleanField(default=True)
    addedOn = models.DateTimeField(auto_now_add=True)
    picture = models.CharField(max_length=250)
    parcelCharge = models.FloatField(default=0.0)

    def __str__(self) -> str:
        return self.name