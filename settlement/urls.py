from django.urls import path
from .views import *

urlpatterns = [
    path('all-unsettled-bills/', getAllUnSettledBills, name="all_unsettled_bills"),
    path('all-settlements/',displayAllSettlements,name='all_settlements'),
]