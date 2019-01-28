
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .productionUpdate import updateProduction
from report.views import dashBoard

@login_required
def Installed_CMM(request):
    return render(request, 'op/Installed_CMM.html')

@login_required
def Installed_each_year_bar(request):
    return render(request,'op/Installed_each_year_bar.html')

@login_required
def Installed_each_year(request):
    return render(request, 'op/Installed_each_year.html')
    
@login_required
def Delivered_CMM(request):
    return render(request, 'op/Delivered_CMM.html')

@login_required
def New_order(request):
    return render(request,'op/New_order.html')

@login_required
def Waiting_Order_and_Inventory(request):
    return render(request, 'op/Waiting_Order_and_Inventory.html')

@login_required
def produced(rquest):
    results = updateProduction()
    dashBoard(rquest)
    return render(rquest, 'op/生产制造.html')

@login_required
def plan(request):
    return render(request, 'op/配置缺件.html')