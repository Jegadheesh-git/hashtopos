from django.urls import path
from .views import *

urlpatterns = [
    path('place-order/',addOrder, name='place_order'),
    path('all-orders/',displayAllOrders,name='all_orders'),
    path('unbilled-orders/',displayAllUnbilledOrders,name='unbilled_orders'),
    path('orders-in-progress/',displayAllInProgressOrders,name='in_progress_orders'),
    path('all-order-timetaken/',displayAllOrdersTimeTaken,name='all_order_time_taken'),
    path('edit-order/<int:pk>/',editOrder,name='edit_order'),
    path('move-to-ready/<int:pk>/',moveToReady,name='move_to_ready'),
    path('parcel-calculator/<int:pk>/',parcelCalculator,name='parcel_calculator'),
]