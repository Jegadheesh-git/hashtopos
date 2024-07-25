from django.urls import path
from .views import *

urlpatterns = [
    path('generate-bill/<int:pk>/',generateBill,name="generate_bill"),
    path('all_bills/',getAllBills,name='get_all_bills'),
]