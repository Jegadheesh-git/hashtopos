from django.shortcuts import render
from billing.models import Bill
from settlement.models import SettlementPercentage, Settlement
from inventory.models import Purchase, PurchaseItem
from expenses.models import Expense
from order.models import Order, OrderItem
from django.db.models import Sum
from django.db.models.functions import TruncDate
from datetime import datetime
from django.utils.dateparse import parse_date
from django.utils import timezone


# Create your views here.
def displaySalesDashboard(request):
    start_date = request.GET.get('start-date')
    end_date = request.GET.get('end-date')
    if start_date and end_date:
        start_date = parse_date(start_date)
        end_date = parse_date(end_date)
        
        # Convert dates to datetime
        start_date = datetime.combine(start_date, datetime.min.time())
        end_date = datetime.combine(end_date, datetime.max.time())

        # Make datetime objects timezone-aware
        start_date = timezone.make_aware(start_date, timezone.get_current_timezone())
        end_date = timezone.make_aware(end_date, timezone.get_current_timezone())

        bills = Bill.objects.filter(dateTime__range=[start_date, end_date])
        sales_data = Order.objects.filter(orderDateTime__range=[start_date, end_date]).values(date=TruncDate('orderDateTime')).annotate(total_sales=Sum('finalPriceIncludedParcel')).order_by('date')
        #sales data by order mode
        om_sales_data = Order.objects.filter(orderDateTime__range=[start_date, end_date]).values('orderMode__name', date=TruncDate('orderDateTime')) \
                              .annotate(total_sales=Sum('finalPriceIncludedParcel')) \
                              .order_by('orderMode__name', 'date')
    
    else:
        bills = Bill.objects.all()
        sales_data = Order.objects.values(date=TruncDate('orderDateTime')).annotate(total_sales=Sum('finalPriceIncludedParcel')).order_by('date')
        #sales data by order mode
        om_sales_data = Order.objects.values('orderMode__name', date=TruncDate('orderDateTime')) \
                              .annotate(total_sales=Sum('finalPriceIncludedParcel')) \
                              .order_by('orderMode__name', 'date')
    
    totalBills = bills.count()
    totalSaleAmount = sum( bill.order.finalPrice for bill in bills )
    totalParcelAmount = sum( bill.order.totalParcelCharge for bill in bills )
    totalCollectionAmount = sum( bill.order.finalPriceIncludedParcel for bill in bills )
    settlementPercentage = float(SettlementPercentage.objects.get(pk=1).sharePercentage)
    totalAmountToBePaid = totalSaleAmount*(settlementPercentage/100) 
    totalAmountToKeep = totalSaleAmount - totalSaleAmount*(settlementPercentage/100)
    totalAmountToBePaidIncludingParcel = totalAmountToBePaid + totalParcelAmount

    #daily sales data
    
    sales_data = [(data['date'].strftime("%Y-%m-%d"), data['total_sales']) for data in sales_data]
    
    #average daily metrics
    total_days = len(sales_data) if len(sales_data)>1 else 1
    average_bills_per_day = totalBills/total_days
    average_sales_per_day = totalCollectionAmount/total_days
    average_hashtopia_share_per_day = totalAmountToBePaid/total_days
    average_fresh_share_per_day = totalAmountToKeep/total_days
    average_hashtopia_payment_per_day = totalAmountToBePaidIncludingParcel/total_days
    

    # Transform the data into a dictionary with order modes as keys
    om_sales_dict = {}
    for data in om_sales_data:
        order_mode = data['orderMode__name']
        date = data['date'].strftime("%Y-%m-%d")
        total_sales = data['total_sales']
        if order_mode not in om_sales_dict:
            om_sales_dict[order_mode] = []
        om_sales_dict[order_mode].append((date, total_sales))

    return render(request,'sales_dashboard.html',
        {
            'totalBills': totalBills,
            'totalSaleAmount': totalSaleAmount,
            'totalParcelAmount': totalParcelAmount,
            'totalCollectionAmount': totalCollectionAmount,
            'totalAmountToBePaid': totalAmountToBePaid,
            'totalAmountToKeep': totalAmountToKeep,
            'settlementPercentage': settlementPercentage,
            'totalAmountToBePaidIncludingParcel': totalAmountToBePaidIncludingParcel,
            'sales_data': sales_data,
            'om_sales_dict': om_sales_dict,
            'average_bills_per_day': average_bills_per_day,
            'average_sales_per_day': average_sales_per_day,
            'average_fresh_share_per_day': average_fresh_share_per_day,
            'average_hashtopia_share_per_day': average_hashtopia_share_per_day,
            'average_hashtopia_payment_per_day': average_hashtopia_payment_per_day,
        }
    )

def getItemDashboard(request):

    start_date = request.GET.get('start-date')
    end_date = request.GET.get('end-date')
    if start_date and end_date:
        start_date = parse_date(start_date)
        end_date = parse_date(end_date)
        
        # Convert dates to datetime
        start_date = datetime.combine(start_date, datetime.min.time())
        end_date = datetime.combine(end_date, datetime.max.time())

        # Make datetime objects timezone-aware
        start_date = timezone.make_aware(start_date, timezone.get_current_timezone())
        end_date = timezone.make_aware(end_date, timezone.get_current_timezone())

        aggregated_data = (
        OrderItem.objects
        .filter(order__orderDateTime__range=[start_date, end_date])
        .values('menuItem__name')
        .annotate(total_quantity_sold=Sum('quantity'))
        .order_by('-total_quantity_sold')  # Order by total quantity sold in descending order

        )

        sales_data = (
        OrderItem.objects
        .filter(order__orderDateTime__range=[start_date, end_date])
        .values('menuItem__name')
        .annotate(total_amount_sold=Sum('finalPrice'))
        .order_by('-total_amount_sold')
        )

    else:
        aggregated_data = (
        OrderItem.objects
        .values('menuItem__name')
        .annotate(total_quantity_sold=Sum('quantity'))
        .order_by('-total_quantity_sold')  # Order by total quantity sold in descending order

        )

        sales_data = (
        OrderItem.objects
        .values('menuItem__name')
        .annotate(total_amount_sold=Sum('finalPrice'))
        .order_by('-total_amount_sold')
        )

    chart_data = []
    for data in aggregated_data:
        chart_data.append([data['menuItem__name'], data['total_quantity_sold']])

    chart_sales_data = []
    for data in sales_data:
        chart_sales_data.append([data['menuItem__name'], data['total_amount_sold']])

    return render(request,'item_dashboard.html',{
                                                'chart_data': chart_data,
                                                'chart_sales_data': chart_sales_data,
                                                 'aggregated_data':aggregated_data,
                                                 'sales_data': sales_data
                                                 })

def purchaseDashboard(request):
    start_date = request.GET.get('start-date')
    end_date = request.GET.get('end-date')
    if start_date and end_date:
        start_date = parse_date(start_date)
        end_date = parse_date(end_date)
        
        # Convert dates to datetime
        start_date = datetime.combine(start_date, datetime.min.time())
        end_date = datetime.combine(end_date, datetime.max.time())

        # Make datetime objects timezone-aware
        start_date = timezone.make_aware(start_date, timezone.get_current_timezone())
        end_date = timezone.make_aware(end_date, timezone.get_current_timezone())

        purchaseQuantityData = (
            PurchaseItem.objects
            .filter(purchase__dateTime__range=[start_date, end_date]) 
            .values('item__name','item__quantityType')
            .annotate(total_quantity_purchased = Sum('quantity'),total_amount_purchased=Sum('totalPrice'))
            .order_by('-total_quantity_purchased')
        )
    else:
        purchaseQuantityData = (
            PurchaseItem.objects
            .values('item__name','item__quantityType')
            .annotate(total_quantity_purchased = Sum('quantity'),total_amount_purchased=Sum('totalPrice'))
            .order_by('-total_quantity_purchased')
        )

        

    return render(request,'purchase_dashboard.html',{'purchaseQuantityData':purchaseQuantityData})

def getIncomeExpenseDashboard(request):

    start_date = request.GET.get('start-date')
    end_date = request.GET.get('end-date')
    if start_date and end_date:
        start_date = parse_date(start_date)
        end_date = parse_date(end_date)
        
        # Convert dates to datetime
        start_date = datetime.combine(start_date, datetime.min.time())
        end_date = datetime.combine(end_date, datetime.max.time())

        # Make datetime objects timezone-aware
        start_date = timezone.make_aware(start_date, timezone.get_current_timezone())
        end_date = timezone.make_aware(end_date, timezone.get_current_timezone())

        settlements = Settlement.objects.filter(dateTime__range=[start_date, end_date])
        purchases = Purchase.objects.filter(dateTime__range=[start_date, end_date])
        expenses = Expense.objects.filter(dateTime__range=[start_date, end_date])


    else:
        settlements = Settlement.objects.all()
        purchases = Purchase.objects.all()
        expenses = Expense.objects.all()

    print(settlements)

    totalPaymentAmount = sum(settlement.paymentRecieved for settlement in settlements) if sum(settlement.paymentRecieved for settlement in settlements)>0 else 1 
    totalPurchaseAmount = sum(purchase.totalPrice for purchase in purchases)
    totalOtherExpenseAmount = sum( expense.amount for expense in expenses )

    totalExpenseAmount = totalPurchaseAmount + totalOtherExpenseAmount

    totalProfitAmount = totalPaymentAmount - totalExpenseAmount
    profitPercentage = round((totalProfitAmount/totalPaymentAmount)*100,2)

    return render(request,'income_expense.html',{
        'totalPaymentAmount':totalPaymentAmount,
        'totalPurchaseAmount': totalPurchaseAmount,
        'totalOtherExpenseAmount': totalOtherExpenseAmount,
        'totalExpenseAmount': totalExpenseAmount,
        'totalProfitAmount': totalProfitAmount,
        'profitPercentage': profitPercentage
        })