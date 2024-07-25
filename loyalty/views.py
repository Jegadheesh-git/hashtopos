from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from order.models import * 
from django.http import JsonResponse

# Create your views here.

def checkCoupon(request):
    couponCode = request.GET.get('couponCode')
    orderId = request.GET.get('orderId')
    couponList = Coupons.objects.filter(name=couponCode)
    if(len(couponList)==1):
        order = get_object_or_404(Order,pk=orderId)
        coupon = couponList[0]
        if coupon.couponType == 'Percentage' and order.totalPrice>=coupon.maximumBillValue:
            finalPrice=0
            for orderItem in order.orderItems.all():
                for offerItem in coupon.items.all():
                    if(orderItem.menuItem.name == offerItem.name):
                        orderItem.finalPrice = orderItem.totalPrice - orderItem.totalPrice*coupon.discountPercentage/100
                        orderItem.save()
                finalPrice += orderItem.finalPrice
            order.finalPrice = finalPrice
            order.finalPriceIncludedParcel = order.finalPrice + order.totalParcelCharge
            order.couponUsed = coupon
            order.hasCouponApplied = True
            order.save()
            return JsonResponse({'message':'Percentage Coupon Applied'})
        elif coupon.couponType == 'Flat' and order.totalPrice>=coupon.maximumBillValue:
            order.finalPrice = order.totalPrice - coupon.flatDiscountAmount
            order.finalPriceIncludedParcel = order.finalPrice + order.totalParcelCharge
            order.couponUsed = coupon
            order.hasCouponApplied = True
            order.save()
            return JsonResponse({'message':'Flat Coupon Applied'})
        else:
            return JsonResponse({'message':'Insufficient Order amount'})
 
        
    else:
        return JsonResponse({'message':'Coupon Doesnot Exists'})
    
def removeCoupon(request):
    order = get_object_or_404(Order,pk=request.GET.get('orderId'))
    for orderItem in order.orderItems.all():
        orderItem.finalPrice = orderItem.totalPrice
        orderItem.save()
    order.finalPrice = order.totalPrice
    order.finalPriceIncludedParcel = order.finalPrice + order.totalParcelCharge
    order.hasCouponApplied = False
    order.couponUsed = None
    order.save()
    return JsonResponse({'message':'Coupon Removed'})

def addCustomerFeedback(request):

    if request.method == 'POST':
        customerName = request.POST.get('customer-name','')
        feedbackType = request.POST.get('feebackType')
        feedbackSummary = request.POST.get('feedbackSummary')

        customerFeedback = CustomerFeedback.objects.create(
            customerName = customerName,
            feedBackType = feedbackType,
            feedbackSummary = feedbackSummary,
            closureSummary = ' '
        )

        customerFeedback.save()

    return render(request,'customer_feedback.html',{'feedbackTypes':['Good review','Taste Issue','Order Delay','Item Add suggestion','Other']})

def getAllCustomerFeedbacks(request):
    customerFeedbacks = CustomerFeedback.objects.all().order_by('-dateTime')
    return render(request,'all_customer_feedbacks.html',{'customerFeedbacks':customerFeedbacks})