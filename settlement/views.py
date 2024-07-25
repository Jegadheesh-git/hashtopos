from django.shortcuts import render, redirect
from billing.models import Bill
from .models import *
from datetime import datetime

# Create your views here.
def getAllUnSettledBills(request):
    bills = Bill.objects.filter(settlementStatus=False).order_by('-dateTime')
    totalSaleAmount = sum( bill.order.finalPrice for bill in bills )
    totalParcelAmount = sum( bill.order.totalParcelCharge for bill in bills )
    totalCollectionAmount = sum( bill.order.finalPriceIncludedParcel for bill in bills )
    settlementPercentage = float(SettlementPercentage.objects.get(pk=1).sharePercentage)
    totalAmountToBePaid = totalSaleAmount*(settlementPercentage/100) 

    totalAmountToKeep = totalSaleAmount - totalSaleAmount*(settlementPercentage/100)

    partiallyPaidSettlements = Settlement.objects.filter(isFullyPaid=False)
    totalBalanceSettlementAmount = sum( settlement.balancePayment for settlement in partiallyPaidSettlements )

    totalAmountToBePaidIncludingParcel = totalAmountToBePaid + totalParcelAmount + totalBalanceSettlementAmount

    if request.method == "POST":
        settlement = Settlement(
            totalSaleAmount = totalAmountToBePaid,
            totalParcelAmount = totalParcelAmount,
            totalPastBalanceAmount = totalBalanceSettlementAmount,
            totalAmountToBeSettled = totalAmountToBePaidIncludingParcel,
            paymentRecieved = float(request.POST.get('paymentAmount')),
            balancePayment = totalAmountToBePaidIncludingParcel - float(request.POST.get('paymentAmount')),
            payerCollectedAmount = totalAmountToKeep,
            isFullyPaid = True if (totalAmountToBePaidIncludingParcel - float(request.POST.get('paymentAmount'))) == 0 else False,
        )
        settlement.save()
        settlement.bills.add(*bills)
        settlement.save()

        for bill in bills:
            bill.settlementStatus = True
            bill.save()
        
        for partiallyPaidSettlement in partiallyPaidSettlements:
            partiallyPaidSettlement.balanceAmountCarryForwardedOn = datetime.now()
            partiallyPaidSettlement.isFullyPaid = True
            partiallyPaidSettlement.save()

        return redirect('all_unsettled_bills')
    
    return render(request,'unsettled_bills.html',{
        'bills':bills,
        'billCount':bills.count(),
        'totalSaleAmount':totalSaleAmount,
        'totalParcelAmount':totalParcelAmount,
        'totalCollectionAmount': totalCollectionAmount,
        'totalAmountToBePaid': totalAmountToBePaid,
        'totalAmountToKeep': totalAmountToKeep,
        'totalAmountToBePaidIncludingParcel': totalAmountToBePaidIncludingParcel,
        'partiallyPaidSettlements': partiallyPaidSettlements,
        'settlementPercentage': settlementPercentage,
        'sharePercentage': 100-settlementPercentage,
        'totalBalanceSettlementAmount': totalBalanceSettlementAmount,
        'modeOfPayments': ['Cash','UPI','Bank Transfer']
        })

def displayAllSettlements(request):
    settlements = Settlement.objects.all()
    return render(request,'all_settlements.html',{'settlements':settlements})

    
