from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from django.http import JsonResponse
import json
from datetime import datetime,date

# Create your views here.

def getAllPurchases(request):
    
    dateVal = request.GET.get('date')
    if not dateVal:
        dateVal = date.today()

    purchases = Purchase.objects.filter(dateTime__date=dateVal).order_by('-dateTime')
    return render(request,'all_purchases.html',{'purchases':purchases})

def purchaseFromVendors(request):
    dailyInventoryCheck = DailyInventoryCheck.objects.all().order_by('-dateTime')[0]
    vendors = Vendor.objects.all()
    vendor_purchases = dict()

    for vendor in vendors:
        phoneNumber = vendor.phoneNumber
        name = vendor.name

        vendorData = {
            'phoneNumber': phoneNumber,
            'purchases': []
        }

        vendor_purchases[name] = vendorData


    for itemToPurchase in dailyInventoryCheck.itemsToPurchase.all():
        itemName = itemToPurchase.item.name
        quantity = itemToPurchase.item.requiredPurchaseQuantity
        quantityType = itemToPurchase.item.quantityType
        vendor_name = itemToPurchase.item.vendor.name
        
        if not itemToPurchase.purchased:
            purchaseDict = {'itemName':itemName,'quantity':quantity,'quantityType':quantityType}

            if vendor_name in vendor_purchases:
                vendor_purchases[vendor_name]['purchases'].append(purchaseDict)

    return render(request,'purchase_vendors.html',{'vendor_purchases':vendor_purchases})
def addPurchase(request):

    if request.method == 'POST':
        vendor = get_object_or_404(Vendor,pk=request.POST.get('vendor'))
        isFullyPaid = request.POST.get('isFullyPaid')
        remarks = request.POST.get('remarks')
        purchase = Purchase.objects.create(totalPrice=0,vendor=vendor,remarks=remarks,isFullyPaid=bool(isFullyPaid))       
        totalPrice = 0
        for key, value in request.POST.items():
            if key.startswith('quantity'):
                itemId = key.split('-')[1]
                item = get_object_or_404(Item,pk=itemId)
                quantity = value
                amount = request.POST.get('amount-'+str(itemId))
                pricePeritem = float(amount)/float(quantity)

                totalPrice += float(amount)
                purchaseItem = PurchaseItem(item=item,quantity=float(quantity),totalPrice=amount,quantityType=item.quantityType,pricePerItem=pricePeritem)
                purchaseItem.save()

                purchase.purchaseItems.add(purchaseItem)
                dailyInventoryCheck = DailyInventoryCheck.objects.all().order_by('-dateTime')[0]

                for itemToPurchase in dailyInventoryCheck.itemsToPurchase.all():
                    print(item,itemToPurchase.item)
                    if itemToPurchase.item == item:
                        print("equal")
                        itemToPurchase.requirmentpurchasedOn = datetime.now()
                        itemToPurchase.purchased = True
                        itemToPurchase.save()

        purchase.totalPrice = totalPrice
        purchase.save()

    vendors = Vendor.objects.all()
    return render(request, "purchase.html",{'vendors':vendors})

def SearchItem(request):
    search_query = request.GET.get("q")
    items = Item.objects.filter(name__icontains=search_query)  # Search by item type name (case-insensitive)

    # Prepare search results data for template
    search_results = items.values('pk','name', 'itemType__name', 'quantity', 'quantityType')  # Select relevant fields

    return JsonResponse({'search_results':list(search_results)})
    

def inventoryCheck(request):
    updatedToday = False
    try:
        dailyInventoryCheck = DailyInventoryCheck.objects.all().order_by('-dateTime')[0]
    
        if dailyInventoryCheck.dateTime.date() == datetime.now().date():
            updatedToday = True
    except:
        pass
    items = Item.objects.all()
    if request.method == 'POST':
        dailyInventoryCheck = DailyInventoryCheck.objects.create(totalRequiredItems=0) 
        totalItemsRequired = 0
        for item in items:
            availability = True if request.POST.get(str(item.pk)) == 'on' else False
            if not availability:
                itemToPurchase = ItemToPurchase(item=item,remarks='')
                itemToPurchase.save()
                totalItemsRequired += 1
                dailyInventoryCheck.itemsToPurchase.add(itemToPurchase)
        dailyInventoryCheck.totalRequiredItems = totalItemsRequired
        dailyInventoryCheck.save()

        return redirect('shopping_todo')

    return render(request,'inventory_check.html',{'items':items,'updatedToday':updatedToday})


def getShoppingList(request):
    dailyInventoryCheck = DailyInventoryCheck.objects.all().order_by('-dateTime')[0]
    
    return render(request,'shopping_todo.html',{'dailyInventoryCheck':dailyInventoryCheck})

def adjustInventory(request):
    if request.method == 'POST':
        wastageType = request.POST.get('wastageType')
        for key, value in request.POST.items():
            if key.startswith('quantity'):
                itemId = key.split('-')[1]
                item = get_object_or_404(Item,pk=itemId)
                quantity = value
                wastage = Wastage(item=item,quantity=quantity,quantityType='Unit',wastageType=wastageType)
                wastage.save()
               

    return render(request,'inventory_adjustments.html',{'wastageTypes':['Expired','Spoiled','Own usage','Missing','Other']})

def getAllInventoryAdjustments(request):
    dateVal = request.GET.get('date')
    if not dateVal:
        dateVal = date.today()
    wastages = Wastage.objects.filter(dateTime__date=dateVal).order_by('-dateTime')
    return render(request,'all_inventory_adjustments.html',{'wastages':wastages})