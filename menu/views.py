from django.shortcuts import render, redirect
from .models import MenuItem
from order.models import OrderMode
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='/login/')
def getAllMenuItems(request):
    
    menu_items_by_category = {}
    for item in MenuItem.objects.select_related('subCategory'):
        category = item.subCategory  # Access parent category
        if category.name not in menu_items_by_category:
            menu_items_by_category[category.name] = []
        menu_items_by_category[category.name].append(item)
    print(menu_items_by_category)
    orderMode = OrderMode.objects.all()
    context = {'menu_items': menu_items_by_category,'orderMode':orderMode}
    return render(request, 'menu.html', context)
    #return render(request,'menu.html',{'menu':menuItems})

