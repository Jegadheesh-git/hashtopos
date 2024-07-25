from django.urls import path
from .views import *

urlpatterns = [
    path('add-expense/',addExpense,name='add_expense'),
    path('all-expenses/',getAllExpenses,name='all_expenses'),
]