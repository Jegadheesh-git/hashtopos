from django.urls import path
from .views import *

urlpatterns = [
    path('add-purchase/',addPurchase,name='add_purchase'),
    path('search/',SearchItem,name='search_item'),
    path('all-purcahses/',getAllPurchases,name='all_purchases'),
    path('inventory-check/',inventoryCheck,name='inventory_check'),
    path('shopping-todo/',getShoppingList,name='shopping_todo'),
    path('inventory-adjustment/',adjustInventory,name='inventory_adjustment'),
    path('all-inventory-adjustments/',getAllInventoryAdjustments,name='all_inventory_adjustments'),
    path('purchase-vendors/',purchaseFromVendors,name='purchase_vendors'),
]