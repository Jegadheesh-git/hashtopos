from django.urls import path
from .views import *

urlpatterns = [
    path('check-coupon/',checkCoupon,name='check_coupon'),
    path('remove-coupon/',removeCoupon,name='remove_coupon'),
    path('add-customer-feedback/',addCustomerFeedback,name='add_customer_feedback'),
    path('get-all-customer-feedbacks/',getAllCustomerFeedbacks,name='get_all_customer_feedbacks'),
]