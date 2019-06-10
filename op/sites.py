
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .productionUpdate import updateProduction
from report.views import dashBoard,updateEchartOp,opCompletTable
from .models import InstalledCmm, DeliveredCmm
from datetime import date
from django.http import HttpResponseRedirect
import calendar

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
    #### update this month data
    today = date.today()
    from_date = today.replace(day=1)
    table = opCompletTable(from_date,today)
    op51,op142 = updateEchartOp(table)
    
    year = today.year
    month = calendar.month_abbr[today.month]
    InstalledCmm.objects.filter(Year=year).update(**{month:op51})
    DeliveredCmm.objects.filter(Year=year).update(**{month:op142})
    results = updateProduction()
    return render(rquest, 'op/生产制造.html')

@login_required
def plan(request):
    return render(request, 'op/配置缺件.html')

@login_required
def onsiteDash(request):
    return HttpResponseRedirect("http://10.135.4.5:8081/WebReport/ReportServer?op=fs")