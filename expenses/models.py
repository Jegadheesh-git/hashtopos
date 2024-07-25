from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class ExpenseType(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.name

class Expense(models.Model):
    expenseType = models.ForeignKey(ExpenseType,on_delete=models.CASCADE)
    description = models.CharField(max_length=250)
    amount = models.FloatField()
    dateTime = models.DateTimeField(auto_now_add=True)
    fromDate = models.DateField(blank=True,null=True)
    toDate = models.DateField(blank=True,null=True)
    addedBy = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.expenseType.name + ' '+ str(self.amount)+ ' '+str(self.dateTime)