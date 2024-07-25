from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(ItemType)
admin.site.register(Item)
admin.site.register(Purchase)
admin.site.register(PurchaseItem)
admin.site.register(Vendor)
admin.site.register(Wastage)
admin.site.register(ItemToPurchase)
admin.site.register(DailyInventoryCheck)