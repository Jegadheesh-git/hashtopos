from django.urls import path
from .views import *

urlpatterns = [
    path('sales-dashboard/',displaySalesDashboard,name='sales_dashboard'),
    path('item-dashboard/',getItemDashboard,name='item_dashboard'),
    path('purchase-dashboard/',purchaseDashboard,name='purchase_dashboard'),
    path('income-expense/',getIncomeExpenseDashboard,name='income_expense_dashboard'),
]