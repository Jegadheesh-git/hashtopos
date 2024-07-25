from django.shortcuts import render, redirect, get_object_or_404
from order.models import *
from .models import *
from datetime import date
from django.db.models import Sum
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='/login/')
def getAllBills(request):
    bills = Bill.objects.filter(dateTime__date=date.today()).order_by('-dateTime')
    orders = Order.objects.filter(orderDateTime__date=date.today()).order_by('-dateTime')
    billCount = bills.count()
    totalAmount = orders.aggregate(total=Sum('finalPriceIncludedParcel'))['total']

    print(totalAmount)
    return render(request,'all_bills.html',{'bills':bills,'billCount':billCount,'totalAmount':totalAmount})

def generateBill(request,pk):
    order = Order.objects.get(pk=pk)
    if order.orderMode.quickBill:
        bill = Bill(
            order=order,
            billedBy=request.user,
            modeOfPayment = 'UPI'
            )
        bill.save()
        order.orderStatus = OrderStatus.objects.get(pk=3)
        order.save()
        return redirect('get_all_bills')
    else:
        if request.method=='POST':
            modeOfPayment = request.POST.get('modeOfPayment')
            customer = request.POST.get('customer')
            if customer != '':            
                try:
                    # Attempt to fetch the customer with the phone number (primary key)
                    customerData = Customer.objects.get(pk=customer)
                    customerData.loyaltyPoints = customerData.loyaltyPoints + order.totalPrice/10
                    customerData.save()
                except Customer.DoesNotExist:
                    # Customer not found, create a new one
                    customerData = Customer(phone=customer,name='',email='',loyaltyPoints=order.totalPrice/10)
                    customerData.save()
            else:
                customerData = None
            bill = Bill(
                    order=order,
                    billedBy=request.user,
                    modeOfPayment = modeOfPayment,
                    customer=customerData
                    )
            bill.save()
            order.orderStatus = OrderStatus.objects.get(pk=3)
            order.save()
            return redirect('get_all_bills')
        else:
            modeOfPayment = ['Cash','UPI','Bank Transfer']
            return render(request,'bill.html',{'order':order,'modeOfPayment':modeOfPayment})