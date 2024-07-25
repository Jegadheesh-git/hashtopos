from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from menu.models import *
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import date,datetime
from django.utils import timezone  # Import timezone utility


# Create your views here.

def createOrder(request):
    menuItems = MenuItem.objects.all()
    orderMode = OrderMode.objects.all()
    context = {'menu_items': menuItems,'orderMode':orderMode}
    return render(request, 'create_order.html', context)


@csrf_exempt
def addOrder(request):

    if request.method == 'POST':
        try:
            orderStatus = OrderStatus.objects.get(pk=1)
            orderMode = get_object_or_404(OrderMode,pk=request.POST.get('orderMode'))
            order = Order.objects.create(orderStatus=orderStatus,takenBy=request.user,totalPrice=0,finalPrice=0.0,orderMode=orderMode)
            totalPrice = 0
            for item in MenuItem.objects.all():
                quantity = request.POST.get(str(item.id))
                if int(quantity)>0:
                    menuItem = get_object_or_404(MenuItem,pk=str(item.id))
                    orderItem = OrderItem(menuItem=menuItem,quantity=quantity,totalPrice=int(quantity)*menuItem.price,finalPrice = int(quantity)*menuItem.price )
                    orderItem.save()
                    order.save()
                    order.orderItems.add(orderItem)
                    totalPrice += int(quantity)*menuItem.price
            order.totalPrice = totalPrice
            order.finalPrice = totalPrice
            order.finalPriceIncludedParcel = totalPrice
            order.save()
               
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid order data format'}, status=400)

        # Access and process order data here
        if order.orderMode.quickBill:
            totalParcelCharge = 0
            for orderItem in order.orderItems.all():
                orderItem.parcelCharge = orderItem.quantity * orderItem.menuItem.parcelCharge
                orderItem.isParcel = True
                orderItem.save()
                totalParcelCharge += orderItem.parcelCharge
            order.totalParcelCharge = totalParcelCharge
            order.finalPriceIncludedParcel = order.totalPrice + totalParcelCharge
            order.save()
            return redirect('in_progress_orders')
        else:
            return redirect('parcel_calculator',order.pk)
    else:
        # Handle non-POST requests (optional)
        return JsonResponse({'error': 'Invalid request method'}, status=405)

def displayAllOrders(request):
    orders = Order.objects.filter(orderDateTime__date=date.today()).order_by('-orderDateTime')
    #orders = Order.objects.all().order_by('-orderDateTime')
    displayName = "Today's All Orders"
    return render(request,'all_orders.html',{'orders':orders,'displayName':displayName})

def displayAllUnbilledOrders(request):
    placed = OrderStatus.objects.get(pk=2)
    orders = Order.objects.filter(orderDateTime__date=date.today(),orderStatus=placed).order_by('-orderDateTime')
    displayName = "Today's Unbilled Orders"
    return render(request,'all_orders.html',{'orders':orders,'displayName':displayName})

def displayAllInProgressOrders(request):
    inProgress = OrderStatus.objects.get(pk=1)
    orders = Order.objects.filter(orderDateTime__date=date.today(),orderStatus=inProgress).order_by('-orderDateTime')
    return render(request,'all_orders.html',{'orders':orders,'displayName':'In Progress Orders'})

def displayAllOrdersTimeTaken(request):
    dateVal = request.GET.get('date')
    if not dateVal:
        dateVal = date.today()

    orders = Order.objects.filter(orderDateTime__date=dateVal).order_by('-orderDateTime')
    return render(request,'all_order_timetaken.html',{'orders':orders})

def moveToReady(request,pk):
    order = Order.objects.get(pk=pk)
    order.orderStatus = OrderStatus.objects.get(pk=2)
    order.orderDeliveredDateTime = timezone.now()
    totalTimeTaken = order.orderDeliveredDateTime - order.orderDateTime
    #totalTimeTaken = abs(totalTimeTaken) / 60
    order.totalTimeTakenForPreparation = totalTimeTaken
    print(totalTimeTaken)
    order.save()
    return redirect('in_progress_orders')

def parcelCalculator(request,pk):
    order = get_object_or_404(Order,pk=pk)
    if request.method == 'POST':
        total_parcel_charge = 0
        note =  str( request.POST.get('note') )
        for orderItem in order.orderItems.all():
            is_parcel = request.POST.get(str(orderItem.pk))
            parcel_qty = int(request.POST.get('pqty'+str(orderItem.pk)))
            
            if is_parcel:
                orderItem.parcelCharge = parcel_qty * orderItem.menuItem.parcelCharge
                total_parcel_charge += orderItem.parcelCharge
                is_parcel = True
            else:
                is_parcel = False  

            orderItem.isParcel = is_parcel
            orderItem.parcelQuantity = parcel_qty
           
            orderItem.save()
        if note != 'None':
            order.note = note
        order.totalParcelCharge = total_parcel_charge
        order.finalPriceIncludedParcel = order.totalPrice + total_parcel_charge
        order.save()
        return redirect('in_progress_orders')
    return render(request,'parcel.html',{'order':order})
        

def editOrder(request,pk):
    if request.method == 'POST':
        print(request.POST)
        status = get_object_or_404(OrderStatus,pk=request.POST.get('status'))
        orderMode = get_object_or_404(OrderMode,pk=request.POST.get('orderMode'))
        order = Order.objects.get(pk=pk)
        order.orderStatus = status
        order.orderMode = orderMode
        order.orderItems.all().delete()
        totalPrice = 0
        for item in MenuItem.objects.all():
            quantity = request.POST.get(str(item.id))
            if int(quantity)>0:
                menuItem = get_object_or_404(MenuItem,pk=str(item.id))
                isParcel = True if request.POST.get('p'+str(item.id),False) == 'on' else False
                orderItem = OrderItem(menuItem=menuItem,quantity=quantity,totalPrice=int(quantity)*menuItem.price,finalPrice=int(quantity)*menuItem.price,isParcel=isParcel)
                orderItem.save()
                order.save()
                order.orderItems.add(orderItem)
                totalPrice += int(quantity)*menuItem.price
        order.totalPrice = totalPrice
        order.finalPrice = totalPrice
        order.save()
        return redirect('parcel_calculator',order.pk)

    else:
        order = Order.objects.get(pk=pk)
        statuses = OrderStatus.objects.all()
        orderModes = OrderMode.objects.all()
        menu_items_by_category = {}
        for item in MenuItem.objects.select_related('subCategory'):
            category = item.subCategory  # Access parent category
            if category.name not in menu_items_by_category:
                menu_items_by_category[category.name] = []
            quantity = 0
            isParcel = False
            for orderItem in order.orderItems.all():
                if orderItem.menuItem.name == item.name:
                    quantity += orderItem.quantity
                    isParcel = orderItem.isParcel
            menu_items_by_category[category.name].append({'item':item,'quantity':quantity,'isParcel':isParcel})
        print(menu_items_by_category)
        context = {'menu_items': menu_items_by_category,'order':order,'statuses':statuses,'orderMode':orderModes}
        return render(request, 'edit_order.html', context)
