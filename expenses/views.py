from django.shortcuts import render, get_object_or_404
from .models import *
# Create your views here.
def addExpense(request):
    if request.method == 'POST':
        expenseType = get_object_or_404(ExpenseType,pk=request.POST.get('expenseType'))
        amount = request.POST.get('amount')
        description = request.POST.get('description')

        expense = Expense.objects.create(expenseType=expenseType,amount=amount,description=description,addedBy=request.user)
        expense.save()

    expenseTypes = ExpenseType.objects.all()
    return render(request,'add_expense.html',{'expenseTypes':expenseTypes})

def getAllExpenses(request):
    expenses = Expense.objects.all().order_by('-dateTime')
    print(expenses)
    return render(request,'all_expenses.html',{'expenses':expenses})
