from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Prob, Op, SfmProd, TypeStandard, Report,SupportiveTime,CoefficientSupport,Borrow,GroupOp,GroupPerform,SfgComments,OverTime,TraceLog,AnnualLeave,UserGroups,DocType,DocInfo,WorkGroups,MaterialApprove,MaterialGet,Material,MeterialUse,MeterialSurplus
from datetime import date, timedelta,datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.http import JsonResponse
# from django.core.serializers import serialize
import json
from calendar import monthrange
import calendar
import numpy as np
from django.template import loader
from pyecharts import Bar
# from django.conf import settings as original_settings
# from django.template import RequestContext
import pandas as pd
import calendar
from .echarts import op_bar,eply_eff_bar,eply_kpi_bar,support_bar,standardTime
from django.db.models import Q
from op.models import InstalledCmm, DeliveredCmm
from time import sleep
import time
import math
from django.template.defaulttags import register

@register.filter(name = 'filter_is_manager')
def filter_is_manager(request):
    groups = ['报工平台-主管']
    return request.user.groups.filter(name__in = groups).exists()

@register.filter(name = 'filter_is_foreman')
def filter_is_foreman(request):
    groups = ['报工平台-班组长']
    manager = ['报工平台-主管']
    return request.user.groups.filter(name__in = groups).exists()

@register.filter(name='filter_is_sczz_manager')
def filter_is_sczz_manager(request):
    groups = ['生产制造-主管']
    return request.user.groups.filter(name__in = groups).exists()

# get standard and real time
@login_required(login_url='/accounts/login/')  
def get_current_date_data(request, result):
    # username = request.user.last_name + request.user.first_name
    # result = Report.objects.filter(user=username, date=date.today())
    list_logs=[]
    standard_time_total = 0
    real_time_total = 0
    quantity_total = 0
    count_total = 0
    for i in range(len(result)):
        a={}
        a['sfg']=result[i].sfg_id
        a['type'] = result[i].type_name
        a['op'] = result[i].op_id
        a['prob'] = result[i].prob
        a['standard'] = result[i].standard_tiem
        a['real'] = result[i].real_time
        a['qty'] = result[i].qty
        # a['over_time'] = result[i].over_time
        # a['over_time_type'] = result[i].over_time_type
        # a['is_paid'] = result[i].is_paid
        a['date'] = result[i].date
        standard_time_total +=a['standard']
        real_time_total += a['real']
        quantity_total += a['qty']
        # overtime_total += a['over_time']
        count_total += 1
        list_logs.append(a)
    a={}
    a['sfg'] = '汇总'
    a['type'] = count_total
    a['op'] = count_total
    a['prob'] = '---'
    a['standard'] = round(standard_time_total,2)
    a['real'] = round(real_time_total,2)
    a['qty'] = round(quantity_total,2)
    # a['over_time'] = round(overtime_total,2)
    # a['over_time_type'] = '---'
    # a['is_paid'] = '---'
    a['date'] = '---'
    list_logs.append(a)

    

    return list_logs, standard_time_total, real_time_total


# get employee's kpi bar chart
@login_required(login_url='/accounts/login/')  
def kpi_dash(request):
    template = loader.get_template('echarts/individul_kpi.html')
    
    
    today = date.today()
    month_first = today.replace(day=1)
    months = []
    kpi_list =  []
    efficiency_list = []
    
    for i in range(today.month):
        month_first = today.replace(month=i+1,day=1)
        last = calendar.monthrange(today.year,i+1)[1]
        month_last = today.replace(month=i+1,day=last)
        # get Report KPI
        result_today = Report.objects.filter(user=request.user.id,date__range=(month_first,month_last))
        list_logs, standard_time_total, real_time_total = get_current_date_data(request, result_today)
        # Get suppotive data
        reuslt_month_supportive = SupportiveTime.objects.filter(user=request.user.id, date__range=(month_first,month_last))
        supportive_logs1,supportive_total1,supportive_total_without_coef1,sup_total_without_coefBorrow,sup_total_without_borrow = get_supportive_history(request, reuslt_month_supportive)
        if real_time_total == 0:
            kpi = 0
        else:
            kpi = round(standard_time_total/real_time_total,2)
        if real_time_total or sup_total_without_coefBorrow:
            efficiency_month = round(real_time_total/(real_time_total + sup_total_without_coefBorrow),2)
        else:
            efficiency_month = 0

        kpi_list.append(kpi)
        months.append(str(i+1))
        efficiency_list.append(efficiency_month)
    bar = Bar("员工工效比",title_top='1%')
    bar.add("工效比", months, kpi_list, legend_pos='40%',legend_top='6%',mark_line_raw=[{'yAxis': 1.2}],is_label_show=True,is_toolbox_show =False)
    bar.add('工时有效率',months,efficiency_list,legend_pos='40%',legend_top='6%',mark_line_raw=[{'yAxis': 0.75}],is_label_show=True,is_toolbox_show =False)

    # context = dict(
    #     kpi_bar=bar.render_embed(),
    #     kpi = kpi,
    #     script_list=bar.get_js_dependencies(),
    # )
    return bar.render_embed()

@login_required(login_url='/accounts/login/')  
def global_context(request):
    username = request.user.id
    today = date.today()
    month_first = today.replace(day=1) #first date of month
    year_first = today.replace(day=1,month=1) #first date of year

    ##get produce worktime
    result_today = Report.objects.filter(user=username, date=today)
    result_this_month = Report.objects.filter(user=username,date__range=(month_first,today))
    result_this_year = Report.objects.filter(user=username,date__range=(year_first,today))

    list_logs, standard_time_total, real_time_total = get_current_date_data(request, result_today)
    list_logs1, standard_time_total1, real_time_total1 = get_current_date_data(request, result_this_month)
    list_logs2, standard_time_total2, real_time_total2 = get_current_date_data(request, result_this_year)

    ## get supportive worktime
    reuslt_today_supportive = SupportiveTime.objects.filter(user=username, date=date.today())
    reuslt_month_supportive = SupportiveTime.objects.filter(user=username, date__range=(month_first,today))
    reuslt_year_supportive = SupportiveTime.objects.filter(user=username, date__range=(year_first,today))

    supportive_logs,supportive_total, supportive_total_without_coef,sup_total_without_coefBorrow,sup_total_without_borrow = get_supportive_history(request, reuslt_today_supportive)
    supportive_logs1,supportive_total1,supportive_total_without_coef1,sup_total_without_coefBorrow1,sup_total_without_borrow = get_supportive_history(request, reuslt_month_supportive)
    supportive_logs2,supportive_total2, supportive_total_without_coef2,sup_total_without_coefBorrow2,sup_total_without_borrow = get_supportive_history(request, reuslt_year_supportive)
    # 工效比
    if real_time_total:
        kpi_today = standard_time_total/real_time_total
    else:
        kpi_today=0
    if real_time_total1:
        kpi_month = standard_time_total1/real_time_total1
    else:
        kpi_month=0
    if real_time_total2:
        kpi_year = standard_time_total2/real_time_total2
    else:
        kpi_year=0
    
    # 工时有效率
    if real_time_total or sup_total_without_coefBorrow:
        efficiency_today = real_time_total/(real_time_total + sup_total_without_coefBorrow)
    else:
        efficiency_today=0
    if real_time_total1 or sup_total_without_coefBorrow1:
        efficiency_month = real_time_total1/(real_time_total1 + sup_total_without_coefBorrow1)
    else:
        efficiency_month=0
    if real_time_total2 or sup_total_without_coefBorrow2:
        efficiency_year = real_time_total2/(real_time_total2 + sup_total_without_coefBorrow2)
    else:
        efficiency_year=0
    # 业绩
    performance_today = standard_time_total + supportive_total

    borrow = Borrow.objects.all()
    probs, ops, group, history_logs, today_kpi, month_kpi, year_kpi,supportive_logs,supportive_total = load_all_data(request)
    
    overtime_data,overtime_data_group,overtime_total = get_overtime(request, username, today,today)
    kpi_dash_data = kpi_dash(request)
    
    all_shown_digits = {
        'g_today_standard_time_total':round(standard_time_total,2),
        'g_today_real_time_total':round(real_time_total,2),
        'g_month_standard_time_total':round(standard_time_total1,2),
        'g_month_real_time_total':round(real_time_total1,2),
        'g_year_standard_time_total':round(standard_time_total2,2),
        'g_year_real_time_total':round(real_time_total2,2),
        'g_today_supportive_total':round(supportive_total,2),
        'g_month_supportive_total':round(supportive_total1,2),
        'g_year_supportive_total':round(supportive_total2,2),
        'kpi_today':round(kpi_today,2),
        'kpi_month':round(kpi_month,2),
        'kpi_year':round(kpi_year,2),
        'efficiency_today':round(efficiency_today,2),
        'efficiency_month':round(efficiency_month,2),
        'efficiency_year':round(efficiency_year,2),
        'performance_today': round(performance_today,2), #业绩
        'borrow_time':borrow, # borrow time category
        'g_today_supportive_total_without_coef': round(supportive_total_without_coef, 2),
        'g_today_natural_hours':round(real_time_total+supportive_total_without_coef,2),
        'op_list':ops,
        'prob_list':probs,
        'groups':group,
        'logs':history_logs,
        # 'today_kpi':today_kpi,
        # 'month_kpi':month_kpi,
        # 'year_kpi':year_kpi,
        'supportive_logs':supportive_logs,
        'supportive_total':round(supportive_total,2),
        'overtime_total':overtime_total,
        'overtime_data':overtime_data.to_html(),
        'kpi_dash_data':kpi_dash_data,
        
        
        
        }

    return all_shown_digits
@login_required(login_url='/accounts/login/') 
def get_supportive_history(request,result):
    supportive_logs=[]
    coef = CoefficientSupport.objects.all()

    list_total = [ [] for i in range(22)]
    list_total_without_coef = [ [] for i in range(22)]
    for i in range(len(list_total)):
        list_total[i] = 0
        list_total_without_coef[i] = 0
    for i in range(len(result)):
        a={}
        a['rest']=result[i].rest
        a['clean'] = result[i].clean_time
        a['inside_group'] = result[i].inside_group
        a['outside_group'] = result[i].outside_group
        a['complete_machine'] = result[i].complete_machine
        a['granite'] = result[i].granite
        a['prob'] = result[i].prob
        a['shortage'] = result[i].shortage
        a['plan_change'] = result[i].plan_change
        a['human_quality_issue_rework']=result[i].human_quality_issue_rework
        a['item_quality_issue'] = result[i].item_quality_issue
        a['human_quality_issue_repair'] = result[i].human_quality_issue_repair
        a['equipment_mantainence'] = result[i].equipment_mantainence
        a['inventory_check'] = result[i].inventory_check
        a['quality_check'] = result[i].quality_check
        a['document'] = result[i].document
        a['group_management'] = result[i].group_management
        a['conference']=result[i].conference
        a['record'] = result[i].record
        a['vertical'] = result[i].vertical
        a['date'] = result[i].date
        a['borrow_time'] = result[i].borrow_time
        a['borrow_name'] = result[i].borrow_name
        a['comments'] = result[i].comments
        list_total[0] += a['rest'] * coef[0].rest
        list_total[1] += a['clean'] * coef[0].clean_time
        list_total[2] += a['inside_group'] * coef[0].inside_group
        list_total[3] += a['outside_group'] * coef[0].outside_group
        list_total[4] += a['complete_machine'] * coef[0].complete_machine
        list_total[5] += a['granite'] * coef[0].granite
        list_total[6] += a['prob'] * coef[0].prob
        list_total[7] += a['shortage'] * coef[0].shortage
        list_total[8] += a['plan_change'] * coef[0].plan_change
        list_total[9] += a['human_quality_issue_rework'] * coef[0].human_quality_issue_rework
        list_total[10] += a['item_quality_issue'] * coef[0].item_quality_issue
        list_total[11] += a['human_quality_issue_repair'] * coef[0].human_quality_issue_repair
        list_total[12] += a['equipment_mantainence'] * coef[0].equipment_mantainence
        list_total[13] += a['inventory_check'] * coef[0].inventory_check
        list_total[14] += a['quality_check'] * coef[0].quality_check
        list_total[15] += a['document'] * coef[0].document
        list_total[16] += a['group_management'] * coef[0].conference
        list_total[17] += a['conference'] * coef[0].group_management
        list_total[18] += a['record'] * coef[0].record
        list_total[20] += a['borrow_time'] * coef[0].borrow_time
        list_total[19] += a['vertical'] * coef[0].vertical
        # get total hours without coefficient
        list_total_without_coef[0] += a['rest'] 
        list_total_without_coef[1] += a['clean'] 
        list_total_without_coef[2] += a['inside_group'] 
        list_total_without_coef[3] += a['outside_group']
        list_total_without_coef[4] += a['complete_machine'] 
        list_total_without_coef[5] += a['granite'] 
        list_total_without_coef[6] += a['prob'] 
        list_total_without_coef[7] += a['shortage']
        list_total_without_coef[8] += a['plan_change'] 
        list_total_without_coef[9] += a['human_quality_issue_rework'] 
        list_total_without_coef[10] += a['item_quality_issue'] 
        list_total_without_coef[11] += a['human_quality_issue_repair'] 
        list_total_without_coef[12] += a['equipment_mantainence'] 
        list_total_without_coef[13] += a['inventory_check'] 
        list_total_without_coef[14] += a['quality_check'] 
        list_total_without_coef[15] += a['document'] 
        list_total_without_coef[16] += a['group_management'] 
        list_total_without_coef[17] += a['conference'] 
        list_total_without_coef[18] += a['record'] 
        list_total_without_coef[20] += a['borrow_time']
        list_total_without_coef[19] += a['vertical']
        
        
        supportive_logs.append(a)
    list_total[21] = '汇总'
    a={}
    for i in range(21):
        list_total[i] = round(list_total[i],2)
    a['rest']=list_total[0]
    a['clean'] =list_total[1]
    a['inside_group'] = list_total[2]
    a['outside_group'] = list_total[3]
    a['complete_machine'] = list_total[4]
    a['granite'] =list_total[5]
    a['prob'] = list_total[6]
    a['shortage'] = list_total[7]
    a['plan_change'] = list_total[8]
    a['human_quality_issue_rework']=list_total[9]
    a['item_quality_issue'] = list_total[10]
    a['human_quality_issue_repair'] = list_total[11]
    a['equipment_mantainence'] = list_total[12]
    a['inventory_check'] = list_total[13]
    a['quality_check'] = list_total[14]
    a['document'] = list_total[15]
    a['group_management'] = list_total[16]
    a['conference'] = list_total[17]
    a['record'] = list_total[18]
    a['vertical'] = list_total[19]
    a['borrow_time'] = list_total[20]
    a['borrow_name'] = '---'
    a['date'] = list_total[21]
    a['comments'] = '---'
    #supportive_total borrow time
    supportive_total = 0 #all with coef
    for i in range(len(list_total)-1):
        supportive_total += list_total[i]
    sup_total_without_borrow = 0  # no borrow with coef
    for i in range(len(list_total)-2):
        sup_total_without_borrow += list_total[i]
    supportive_logs.append(a)
    supportive_total_without_coef = 0  #all without coef
    for i in range(len(list_total_without_coef)):
        supportive_total_without_coef += list_total_without_coef[i]
    sup_total_without_coefBorrow = 0 #no borrow without coef
    for i in range(len(list_total_without_coef)-2):
        sup_total_without_coefBorrow += list_total_without_coef[i]
    return supportive_logs, round(supportive_total,2), round(supportive_total_without_coef, 2), round(sup_total_without_coefBorrow,2), round(sup_total_without_borrow,2),

@login_required(login_url='/accounts/login/')  
def get_kpi(request,result):
    # username = request.user.last_name + request.user.first_name
    # result_today = Report.objects.filter(user=username, date=date.today())
    kpi_today, standard_time_total, real_time_total = get_current_date_data(request,result)
    real_time_today =0
    stand_tiem_today =0
    for i in kpi_today:
        real_time_today += i['real']
        stand_tiem_today += i['standard']
    return real_time_today, stand_tiem_today


@login_required(login_url='/accounts/login/')  
def load_all_data(request):
    probs = Prob.objects.all()
    ## get all user groups
    # user_all_permissions = []
    # user = User.objects.get(id=request.user.id)
    # groups = user.groups
    # for i in groups.select_related():
    #     if '数据' in i.name:
    #         user_all_permissions.append(i.name)

    # get worker user's only one workgroup
    user_group=user_work_group(request)
    ops = []
    # for i in user_all_permissions:
    op = GroupOp.objects.filter(group_name=user_group)
    for i in range(len(op)):
        ops.append(op[i].op_id)
    ops = list(set(ops))

    # check if use is inspector
    groups = request.user.groups.all().values()
    group=None
    for i in groups:
        if '检验员' in i['name']:
            group = 1
       #get current username and report history for today
    #today date
    today = date.today()
    month_first = today.replace(day=1) #first date of month
    year_first = today.replace(day=1,month=1) #first date of year
    username = request.user.id
    # get data for KPI
    result_today = Report.objects.filter(user=username, date=date.today())
    result_this_month = Report.objects.filter(user=username,date__range=(month_first,today))
    result_this_year = Report.objects.filter(user=username,date__range=(year_first,today))
    history_logs, standard_time_total, real_time_total = get_current_date_data(request,result_today)
    
    # day kpi
    real_time_today, stand_time_today = get_kpi(request,result_today)
    if real_time_today and stand_time_today:
        today_kpi = round(stand_time_today/real_time_today,2)
    else:
        today_kpi=0

    real_time_month, stand_time_month = get_kpi(request, result_this_month)
    if real_time_month and stand_time_month:
        month_kpi = round(stand_time_month/real_time_month,2)
    else:
        month_kpi = 0

    real_time_year, stand_time_year = get_kpi(request, result_this_year)
    if real_time_year and stand_time_year:
        year_kpi = round(stand_time_year/real_time_year,2)
    else:
        year_kpi=0

    reuslt_today_supportive = SupportiveTime.objects.filter(user=username, date=date.today())
    supportive_logs,supportive_total, supportive_total_without_coef,sup_total_without_coefBorrow, sup_total_without_borrow = get_supportive_history(request, reuslt_today_supportive)
    
    return probs, ops, group, history_logs, today_kpi, month_kpi, year_kpi,supportive_logs, round(supportive_total,2)

# when load the page
@login_required(login_url='/accounts/login/')  
def index(request):
    
    all_show_digts = global_context(request)

   
    return render(request, 'report/report_get.html', all_show_digts)

# when click submit to save overtime data to database
@login_required(login_url='/accounts/login/')  
def save_overtime_data(request):
    user = request.user.id
    over_time= request.GET.get('over_time')
    over_time_type = request.GET.get('over_type')
    is_paid = request.GET.get('is_paid')
    date =  request.GET.get('date')
    f_user = User.objects.get(id=user)
    user_group = user_work_group(request)
    if is_paid=='true':
        is_paid=1
    else:
        is_paid=0
    date_submit = datetime.strptime(date,"%Y-%m-%d").date()
    perform_history = GroupPerform.objects.filter(date=date_submit,username=request.user.id)
        
    if not perform_history:
        try:
            query=OverTime(user=f_user,over_time=over_time,over_time_type=over_time_type,is_paid=is_paid,date=date,groups=user_group)
            query.save()
            check='Y'
            test_log_duplication(request.user.id,request.user.get_full_name(),'添加加班 Successful','加班种类 '+over_time_type +',付钱：'+str(is_paid)+',加班数：'+
            str(over_time),'时间： '+str(over_time)+', Date: '+date +' is_Paid: '+str(is_paid))
            return HttpResponse(json.dumps(check), content_type='application/json')
        except Exception as ex:    
            template = "加班工时保存失败"
            message = template + json.dumps(ex.args)
            test_log_duplication(request.user.id,request.user.get_full_name(),'Overtime '+over_time_type,'Failed','时间： '+str(over_time)+', Date: '+date +' is_Paid: '+str(is_paid))
            return HttpResponse(json.dumps(message), content_type='application/json')
    else:
        test_log_duplication(request.user.id,request.user.get_full_name(),'Overtime add after submit',' Failed, 加班种类 '+over_time_type +',付钱：'+str(is_paid)+',加班数：'+
            str(over_time),'时间： '+str(over_time)+', Date: '+date +' is_Paid: '+str(is_paid))
        return HttpResponse(json.dumps('保存失败！该日期的报工已经被班组长提交，未防止业绩受损，请联系班组长删除该业绩后再进行提交！'),content_type='application/json')
#### save log in trace log table
def test_log_duplication(user,username,action,detail,comments):
    try:
        f_user = User.objects.get(id=user)
        query = TraceLog(user=f_user,username=username,action_log=action,detail_message=detail,
            comments=comments)
        query.save()
    except Exception as ex:
        f_user = User.objects.get(id=user)
        query = TraceLog(user=f_user,username=username,action_log='save',detail_message='Failed',
            comments=json.dumps(ex.args))
        query.save()

# get IP
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

# get login user's work groups in UserGroup table
def user_work_group(request):
    user = UserGroups.objects.filter(user=request.user.id)
    if user:
        user_group = user[0].work_group.group_name
        return user_group
    else:
        return "没有分组"

# get user's work groups according to Report and Supportive
def user_work_group_ids(group,date):
    all_user_ids = []
    if group:

        users = Report.objects.filter(groups=group,date=date)
        users2= SupportiveTime.objects.filter(groups=group,date=date)
        for i in range(len(users)):
            all_user_ids.append(users[i].user.id)
        for i in range(len(users2)):
            all_user_ids.append(users2[i].user.id)
        all_user_ids=list(set(all_user_ids))
        return all_user_ids
    else:
        return None

#### get usr's ids accroding to work group
def workGroupId(group):
    all_ids = []
    if group:
        f_group = WorkGroups.objects.get(group_name=group)
        results = UserGroups.objects.filter(work_group=f_group)
        for i in range(len(results)):
            all_ids.append(results[i].user.id)
        
    return all_ids
        
# save produce worktime
@login_required(login_url='/accounts/login/')  
def get_data(request):
    try:
        ie = request.META['HTTP_USER_AGENT']
        if "Chrome" not in ie:
            return render(request, 'report/down_chrome.html')
    except:

        pass
    sfg = request.GET.get('sfg_id')
    sfg = str(sfg).strip().upper()
    type = request.GET.get('prod_type')
    op_id = request.GET.get('op_id')
    prob_info = request.GET.get('prob_info')
    #user = request.GET.get('user_name')
    # standard_time = request.GET.get('standard_time']
    real_time = request.GET.get('real_time')
    qty = request.GET.get('qty')
    # over_time= request.GET.get('over_time']
    # over_time_type = request.GET.get('over_time_type']
    # is_paid = request.POST.get('is_paid')
    date_time = request.GET.get('prodate')
    user_group = user_work_group(request)
    # check if standard time exist
    if prob_info == 'None':
        prob = None
        try:
            standart_time = TypeStandard.objects.get(op_id=op_id,type_name=type,prob_info=prob).standard_time 
            standard_time = float(standart_time) * float(qty)
            
        except:
            return HttpResponse('标准工时不存在，请刷新网页！')
        
    
    else:
        try:
            prob_id = Prob.objects.get(prob_info=prob_info)
            standart_time = TypeStandard.objects.get(op_id=op_id,type_name=type,prob_info=prob_id).standard_time
            standard_time = float(standart_time) * float(qty)
        except:
            return HttpResponse('标准工时不存在，请刷新网页！')
    #load data
    
    if prob_info== 'None':
        prob_info=''
    if prob_info == '---':
        prob_info=None
    if prob_info == '空':
        prob_info=None
    # if not over_time:
    #     over_time=0
    # if not is_paid:
    #     is_paid='N'
    # else:
    #     is_paid='Y'
    
    # check if qty is larger than one
    qty_check = True
    result = Report.objects.filter(sfg_id=sfg)
    if len(result) !=0 and int(op_id) != 11:
        total = 0
        for i in range(len(result)):
            if result[i].op_id.op_id == int(op_id):
                total += result[i].qty
        total = 1-total
        if total <=0:
            qty_check = False
    
    if qty_check:
        date_submit = datetime.strptime(date_time,"%Y-%m-%d").date()
        perform_history = GroupPerform.objects.filter(date=date_submit,username=request.user.id)
        
        if not perform_history:
            # return HttpResponse('not able to find history'+date_time+', id is ' + str(user))
            try:
                #f_sfg = SfmProd.objects.get(sfg_id=sfg)
                f_op = Op.objects.get(op_id=op_id)
                f_user = User.objects.get(id=request.user.id)
                query = Report(sfg_id=sfg,type_name=type,op_id=f_op,prob=prob_info,qty=qty,user=f_user,standard_tiem=standard_time,real_time=real_time,
                date=date_time,groups=user_group)
                query.save()

                today = date.today()
                year = today.year
                input_month = datetime.strptime(date_time,"%Y-%m-%d")
                month = calendar.month_abbr[input_month.month]
                last_day = calendar.monthrange(year,input_month.month)

                ## save to InstalledCmm, DeliveredCmm
                # sleep(0.5)
                if op_id=='51' or op_id=='142':
                    # # return HttpResponse('Yes 51')
                    # sfg_qty = Report.objects.filter(sfg_id=sfg,op_id_id=5).values_list('qty')
                    # sfg_qty_total = 0
                    # if len(sfg_qty) !=0:
                    #     for i in range(len(sfg_qty)):
                    #         sfg_qty_total += sfg_qty[i][0]
                    # result = InstalledCmm.objects.filter(Year=year).values()
                    # if len(result) == 0:
                    #     query = InstalledCmm(Year=year,Jan=0,Feb=0,Mar=0,Apr=0,May=0,Jun=0,Jul=0,Aug=0,Sep=0,Oct=0,Nov=0,Dec=0)
                    #     query.save()
                    # # string = "sfg: " + str(sfg_qty_total) + ', qty: ' + str(qty) + ", total: " + str(round(sfg_qty_total+float(qty), 3))
                    # # return HttpResponse(string)
                    # if round(sfg_qty_total,3) ==1: 
                    #     total = result[0][month]
                    #     total += 1
                    #     # return HttpResponse(total)
                    #     InstalledCmm.objects.filter(Year=year).update(**{month:total})
                    op_table=opCompletTable(input_month.replace(day=1),input_month.replace(day=last_day[1]))
                    if len(op_table) != 0:
                        op51,op142 = updateEchartOp(op_table)
                        InstalledCmm.objects.filter(Year=year).update(**{month:op51})
                        DeliveredCmm.objects.filter(Year=year).update(**{month:op142})
                # if op_id=='142':
                
                #     sfg_qty = Report.objects.filter(sfg_id=sfg,op_id_id=16).values_list('qty')
                #     sfg_qty_total = 0
                #     if len(sfg_qty) != 0:
                #         for i in range(len(sfg_qty)):
                #             sfg_qty_total += sfg_qty[i][0] 
                #     result_deli = DeliveredCmm.objects.filter(Year=year).values()
                #     if len(result_deli) == 0:
                #         query = DeliveredCmm(Year=year,Jan=0,Feb=0,Mar=0,Apr=0,May=0,Jun=0,Jul=0,Aug=0,Sep=0,Oct=0,Nov=0,Dec=0)
                #         query.save()
                #     if round(sfg_qty_total,3) ==1:
                #         total = result_deli[0][month]
                #         total += 1
                #         # return HttpResponse(total)
                #         DeliveredCmm.objects.filter(Year=year).update(**{month:total})
                
                
                # all_show_digits = global_context(request)
                save_message="保存成功"
                # local_jason = {
                    
                #     'save_message':save_message,
                    
                #     # 'supportive_logs':supportive_logs,
                #     # 'supportive_total':supportive_total,

                # }

                
                # all_dict = local_jason.copy()
                # all_dict.update(all_show_digits)
                
                # ip = get_client_ip(request)
                test_log_duplication(request.user.id,request.user.get_full_name(),'Report add',str(sfg) +', 工步: '+str(op_id)+" , "  +' Date: '+date_time +', 数量为: '+str(qty),'Type:'+type+ ', Probe:' + prob_info)
                
                return HttpResponse(json.dumps(save_message), content_type='application/json')
                #return render(request, 'report/report_get.html', all_dict)
            except Exception as ex:    
                template = "保存失败"
                message = template + json.dumps(ex.args)
                # save failed message 
                # ip = get_client_ip(request)
                test_log_duplication(request.user.id,request.user.get_full_name(),message,str(sfg) +',:工步'+str(op_id) +', Date: '+date_time +'数量为: '+str(qty),'Type:'+type+ ', Probe:' + prob_info)
                # all_show_digits = global_context(request)
                # local_jason1 = {
                    
                #     'error_message':message,
                #     # 'supportive_logs':supportive_logs,
                #     # 'supportive_total':supportive_total,
                # }
                
                
                # all_dict1 = local_jason1.copy()
                # all_dict1.update(all_show_digits)
                # return HttpResponseRedirect("#")
                return HttpResponse(json.dumps(message), content_type='application/json')
        else:
            test_log_duplication(request.user.id,request.user.get_full_name(),'Report add after submit','Falied, '+str(sfg) +', 工步: '+str(op_id)+" , "  +' Date: '+date_time +', 数量为: '+str(qty),'Type:'+type+ ', Probe:' + prob_info)
            return HttpResponse('保存失败！该日期的报工已经被班组长提交，未防止业绩受损，请联系班组长删除该业绩后再进行提交！')
    else:
        f_user = User.objects.get(id=request.user.id)
        # ip = get_client_ip(request)
        # username = request.user.get_full_name()
        action_log = '制造工时Qty多次提交' 
        detail_message = "Failed"
        comments = str(sfg) +':工步'+str(op_id)+" Failed, "  +'Date: '+date_time +'Date: '+date_time +'数量为: '+str(qty)
        test_log_duplication(request.user.id,request.user.get_full_name(),action_log,detail_message,comments)
        # query = TraceLog(user=f_user,username=username,action_log=action_log,detail_message=detail_message,comments=comments)
        # query.save()
        message = '数量已经为1，无法再添加，请联系班组长进行修改！'
        # return render(request, 'report/report_get.html',{
        #     'error_message':message,
        # })
        #return HttpResponse(json.dumps(message), content_type='application/json')
        return HttpResponse(message)
        
    #制造工时
    # real_time = request.POST['real_time']

    # return render(request,'report/report_get.html',{
    #     'save_message':save_message,
    #     'logs':history_logs,
    # })
    # except:
    #     return render(request,'report/report_get.html',{
    #         'op':ops,
    #         'prob':probs,
    #     })
        
    #     return HttpResponse(isinstance(real_time,float))


# when click submit to save supportive data
@login_required(login_url='/accounts/login/')  
def supportive_time(request):

    rest = request.GET.get('rest')
    clean = request.GET.get('clean')
    record = request.GET.get('record')
    inside_group = request.GET.get('inside_group')
    outside_group = request.GET.get('outside_group')
    complete_machine = request.GET.get('complete_machine')
    granite = request.GET.get('granite')
    prob = request.GET.get('prob')
    shortage = request.GET.get('shortage')
    plan_change = request.GET.get('plan_change')
    human_quality_issue_rework = request.GET.get('human_quality_issue_rework')
    item_quality_issue = request.GET.get('item_quality_issue')
    human_quality_issue_repair = request.GET.get('human_quality_issue_repair')
    equipment_mantainence = request.GET.get('equipment_mantainence')
    inventory_check = request.GET.get('inventory_check')
    quality_check = request.GET.get('quality_check')
    document = request.GET.get('document')
    conference = request.GET.get('conference')
    group_management = request.GET.get('group_management')
    borrow_time = request.GET.get('borrow_time')
    borrow_type = request.GET.get('borrow_type')
    vertical = request.GET.get('vertical')
    comments = request.GET.get('comments')
    date_time = request.GET.get('suportdate')
    user_group = user_work_group(request)
    if not rest:
        rest=0
    if not clean:
        clean=0
    if not inside_group:
        inside_group = 0
    if not record:
        record = 0
    if not outside_group:
        outside_group = 0
    if not complete_machine:
        complete_machine = 0
    if not granite:
        granite = 0
    if not prob:
        prob = 0
    if not shortage:
        shortage = 0
    if not plan_change:
        plan_change = 0
    if not human_quality_issue_rework:
        human_quality_issue_rework = 0
    if not item_quality_issue:
        item_quality_issue = 0
    if not human_quality_issue_repair:
        human_quality_issue_repair = 0
    if not equipment_mantainence:
        equipment_mantainence = 0
    if not inventory_check:
        inventory_check = 0
    if not quality_check:
        quality_check = 0
    if not document:
        document = 0
    if not conference:
        conference = 0
    if not group_management:
        group_management = 0
    if not borrow_time:
        borrow_time = 0
    if not comments:
        comments = ''
    if borrow_type == ' ':
        borrow_type='无外借种类'
    if not vertical:
        vertical=0


    date_submit = datetime.strptime(date_time,"%Y-%m-%d").date()
    perform_history = GroupPerform.objects.filter(date=date_submit,username=request.user.id)
        
    if not perform_history:
        try:    

            f_user = User.objects.get(id=request.user.id)
            query = SupportiveTime(user=f_user,rest=rest,clean_time=clean,inside_group=inside_group,outside_group=outside_group,
            complete_machine=complete_machine,granite=granite,prob=prob,shortage=shortage,plan_change=plan_change,
            human_quality_issue_rework=human_quality_issue_rework,item_quality_issue=item_quality_issue,human_quality_issue_repair=human_quality_issue_repair,
            equipment_mantainence=equipment_mantainence,inventory_check=inventory_check,quality_check=quality_check,
            document=document,conference=conference,group_management=group_management,record=record,date=date_time,borrow_time=borrow_time,borrow_name=borrow_type,
            comments=comments,groups=user_group,vertical=vertical)

            query.save()
            # ip = get_client_ip(request)
            test_log_duplication(request.user.id,request.user.get_full_name(),'Support Add','休息:'+str(rest)+',卫生：'+str(clean)+',组内:'+str(inside_group)+
            ',组外:'+str(outside_group)+',整机：'+str(complete_machine)+',大理石：'+str(granite)+',物流：'+str(prob)+',缺件'+str(shortage)+'计划调整：'+str(plan_change)+
            ',人为：'+str(human_quality_issue_rework)+'，零件：'+str(item_quality_issue),'人为：'+str(human_quality_issue_repair)+'，设备：'+str(equipment_mantainence)+
            ',库存：'+str(inventory_check)+',质量：'+str(quality_check)+'，档案：'+str(document)+',会议：'+str(conference)+'，班组：'+str(group_management)+
            ',线性：'+str(vertical)+',外借：'+str(borrow_time)  +'Date: '+date_time)
            save_message="辅助工时保存成功"
            # get global info
            # all_show_digits = global_context(request)
            # local_jason = {
                
            #     'supportive_save_message':save_message,
            #     'save_message':save_message,
            #     # 'supportive_logs':supportive_logs,
            #     # 'supportive_total':supportive_total,

            # }
            # all_dict = local_jason.copy()
            # all_dict.update(all_show_digits)
            # return render(request, 'report/report_get.html', all_dict)
            return HttpResponse(json.dumps(save_message), content_type='application/json')
        except Exception as ex:    
            template = "保存失败"
            message = template + json.dumps(ex.args)
            # ip=get_client_ip(request)
            # test_log_duplication(request.user.id,request.user.get_full_name(),'Support Add',"Failed",'Failed '+json.dumps(ex.args) +'Date: '+date_time)
            # local_jason = {
            
            #     'supportive_error_message':message,
            #     # 'supportive_logs':supportive_logs,
            #     # 'supportive_total':supportive_total,
            # }
            # all_show_digits = global_context(request)
            # all_dict = local_jason.copy()
            # all_dict.update(all_show_digits)
            # return render(request, 'report/report_get.html', all_dict)
            return HttpResponse(json.dumps(message), content_type='application/json')
        
    else:
        test_log_duplication(request.user.id,request.user.get_full_name(),'Support add after submit','Failed, 休息:'+str(rest)+',清洁：'+str(clean)+',组内:'+str(inside_group)+
            ',组外:'+str(outside_group)+',整机：'+str(complete_machine)+',大理石：'+str(granite)+',物流：'+str(prob)+',缺件'+str(shortage)+'计划调整：'+str(plan_change)+
            ',人为：'+str(human_quality_issue_rework)+'，零件：'+str(item_quality_issue),'人为返修：'+str(human_quality_issue_repair)+'，设备：'+str(equipment_mantainence)+
            ',库存：'+str(inventory_check)+',质量：'+str(quality_check)+'，档案：'+str(document)+',会议：'+str(conference)+'，班组：'+str(group_management)+
            ',线性：'+str(vertical)+',外借：'+str(borrow_time)  +'Date: '+date_time)
        return HttpResponse('保存失败！该日期的报工已经被班组长提交，未防止业绩受损，请联系班组长删除该业绩后再进行提交！')

        # return render(request, 'report/report_get.html',{
    #     'save_message':"successful",
    #     'borrow':borrow_time,
    # })


# get sfg product type name
@login_required(login_url='/accounts/login/')  
def get_sfgid(request):
    a = request.GET.get('a')
    results = []
    try:
        type = SfmProd.objects.filter(sfg_id=a)
        for i in range(len(type)):
            results.append(type[i].type_name)
        if len(results) == 0:
            results.append('找不到SFG ID')
    except:
        #type='找不到SFG ID'
        results.append('找不到SFG ID')

    return_json = {'result':results}
    return HttpResponse(json.dumps(return_json), content_type='application/json')

# get standard time
@login_required(login_url='/accounts/login/')  
def get_standard_time(request):
    type = request.GET.get('type')
    op = request.GET.get('op')
    prob = request.GET.get('prob')
    qty = request.GET.get('qty')
    # no prob info
    if prob == 'None':
        prob = None
        try:
            standart_time = TypeStandard.objects.get(op_id=op,type_name=type,prob_info=prob).standard_time 
            standart_time = float(standart_time) * float(qty)
            result = {'result':round(standart_time,2)}
        except:
             result = {'result':'无标准工时'}
        return HttpResponse(json.dumps(result), content_type='application/json')
    
    else:
        try:
            prob_id = Prob.objects.get(prob_info=prob)
            standart_time = TypeStandard.objects.get(op_id=op,type_name=type,prob_info=prob_id).standard_time
            standart_time = float(standart_time) * float(qty) 
            standart_time = round(standart_time,2) 
            result = {'result':round(standart_time,2)}
        except:
            result = {'result':'无标准工时'}
        return HttpResponse(json.dumps(result), content_type='application/json')

# get login user's all original groups
def get_groups(request):
    user_all_permissions = []
    user = User.objects.get(id=request.user.id)
    groups = user.groups
    for i in groups.select_related():
        user_all_permissions.append(i.name)

    return user_all_permissions

# def get_origin_group(ids):
    

#get all op_ids and all_user_ids in 统计表 accroding to login user's original groups. For finding users in foreman groups
def analysis_op_user(request):
    username = request.user.username
    #result = Report.objects.filter(user=username,date__range=(from_date,to_date)).order_by('date')
    all_work_groups = []
    wgroup_data = WorkGroups.objects.all().values()
    for i in range(len(wgroup_data)):
        all_work_groups.append(wgroup_data[i]['group_name'])

    user_groups = []
    all_user=['testa','testb','testp','testsm','teste']
    if username in all_user:
        group = UserGroups.objects.get(user=request.user.id)
        user_groups.append(group.work_group.group_name)
    else:
        data_groups = get_groups(request)
        for i in range(len(data_groups)):
                if '数据' in data_groups[i]:
                    user_groups.append(data_groups[i])
    all_user_ids = []
    all_op_id = []


    
    # user_manager_group = []

    # user_manager_result = User.objects.filter(groups__name='报工平台-主管')
    # for i in range(len(user_manager_result)):
    #     user_manager_group.append(user_manager_result[i].id)

    for j in range(len(user_groups)):
        if '数据-装配组A' in user_groups[j]:
            users = User.objects.filter(groups__name='数据-装配组A')
            for i in range(len(users)):
                all_user_ids.append(users[i].id)

            ops = GroupOp.objects.filter(group_name='数据-装配组A')
            for i in range(len(ops)):
                all_op_id.append(ops[i].op_id)
            # all_user_ids += user_group_a
            # all_op_id +=ops_group_a

        if '数据-装配组B' in user_groups[j]:
            users = User.objects.filter(groups__name='数据-装配组B')
            for i in range(len(users)):
                all_user_ids.append(users[i].id)

            ops = GroupOp.objects.filter(group_name='数据-装配组B')
            for i in range(len(ops)):
                all_op_id.append(ops[i].op_id)
            # all_user_ids +=user_group_b
            # all_op_id += ops_group_b

        if '数据-电气' in user_groups[j]:
            users = User.objects.filter(groups__name='数据-电气')
            for i in range(len(users)):
                all_user_ids.append(users[i].id)

            ops = GroupOp.objects.filter(group_name='数据-电气')
            for i in range(len(ops)):
                all_op_id.append(ops[i].op_id)
            # all_user_ids += user_group_elc
            # all_op_id += ops_group_elc

        if '数据-包装' in user_groups[j]:
            users = User.objects.filter(groups__name='数据-包装')
            for i in range(len(users)):
                all_user_ids.append(users[i].id)
            
            ops = GroupOp.objects.filter(group_name='数据-包装')
            for i in range(len(ops)):
                all_op_id.append(ops[i].op_id)

            # all_user_ids += user_group_p
            # all_op_id += ops_group_p

        if '数据-装配组SM' in user_groups[j]:
            users = User.objects.filter(groups__name='数据-装配组SM')
            for i in range(len(users)):
                all_user_ids.append(users[i].id)
            
            ops = GroupOp.objects.filter(group_name='数据-装配组SM')
            for i in range(len(ops)):
                all_op_id.append(ops[i].op_id)
            # all_user_ids += user_group_sm
            # all_op_id += ops_group_sm
    all_user_ids = list(set(all_user_ids))
    all_op_id = list(set(all_op_id))
    user_manager_group = []

    user_manager_result = User.objects.filter(groups__name='报工平台-主管')
    for i in range(len(user_manager_result)):
        user_manager_group.append(user_manager_result[i].id)    

    #### sort op id ######
    op_id_ids = []
    for i in range(len(all_op_id)):
        op_id_ids.append(all_op_id[i].op_id)
    
    op_id_ids.sort()

    op_id_sorted = []
    for i in range(len(op_id_ids)):
        a = Op.objects.get(op_id=op_id_ids[i])
        op_id_sorted.append(a)

    # get Op name
    if user_manager_group:
        for i in range(len(user_manager_group)):
            if user_manager_group[i] in all_user_ids:
                all_user_ids.remove(user_manager_group[i])
                
    ##### hide user itself id######

    # if username in all_user_ids:
    #     all_user_ids.remove(username)

    if 1 in all_user_ids:
        all_user_ids.remove(1)
    if len(user_groups) >2:
        user_groups.append('ALL')
        all_work_groups.append('ALL')
   
    return all_user_ids, op_id_sorted,user_groups,all_work_groups

# check if use is report module manager
def is_report_manager(request):
    check = False
    data_groups = get_groups(request)
    for i in range(len(data_groups)):
            if '报工平台-主管' in data_groups[i]:
                check = True
                break
    return check
    

# produce schedule, performance and analyze table信息应用模块
def report_analysis(request):
    from_date = request.POST.get('schedule_from_date')
    to_date = request.POST.get('schedule_to_date')
    p_today = request.POST.get('p_perform_today')
    tab = request.GET.get('tab')
    today = date.today()
    a_month = request.POST.get('a_month')
    a_year = date.today().year
    
    is_manager = is_report_manager(request)
    if not from_date and is_manager:
        from_date = date.today() - timedelta(days=20)
    if not from_date:
        from_date = date.today() - timedelta(days=60)
    if not to_date:
        to_date = date.today()
    if not a_month:
        a_month=today.month
    else:
        a_month = int(a_month)

 
    all_user_ids, all_op_id, user_groups,all_work_groups = analysis_op_user(request)
    
    # if user_manager_group:
    #     for i in range(len(user_manager_group)):
    #         if user_manager_group[i] in all_user_ids:
    #             all_user_ids.remove(user_manager_group[i])
    # if username in all_user_ids:
    #     all_user_ids.remove(username)

    # if 1 in all_user_ids:
    #     all_user_ids.remove(1)

    work_group = user_work_group(request)
    is_electronic = False
    orginal_group = get_groups(request)
    if any('班组长' and '电气' in word for word in orginal_group):
        is_electronic = True
    
    if len(all_user_ids) != 0 and len(all_op_id) != 0:
        # if request.user.id==9:
            # sm_op_ids = GroupOp.objects.filter(group_name='数据-装配组SM')
            # sm_op_id = []
            # for i in range(len(sm_op_ids)):
            #     all_op_id.append(sm_op_ids[i].op_id)
            
        ###++++++++++++++++    version 12-29
        # items = Report.objects.filter(user_id__in=all_user_ids,op_id__in=all_op_id,date__range=(from_date,to_date)).order_by('date').values()#.filter(op_id__in=all_op_id).filter(date__range=(from_date,to_date)).order_by('date')
        ####+++++++++++++++
        
        ##++++++++According to Work Group to filter the schedule results++++++
        if is_manager or is_electronic:
            items = Report.objects.filter(groups__in=user_groups,date__range=(from_date,to_date)).order_by('-date').values()
        else:
            items = Report.objects.filter(groups=work_group,date__range=(from_date,to_date)).order_by('-date').values()
        #data = pd.DataFrame(list(items), columns=['sfg_id','type_name','op_id_id','user_id','date'])
        # data = pd.DataFrame()
        # for i in range(len(items)):
        #     data = data.append({'sfg':items[i].sfg_id, 'type':items[i].type_name,'op':items[i].op_id,'user':items[i].user,'date':items[i].date}, ignore_index=True)
        #     # data['op'][0].op_id
            # data['user'][0].last_name
            # data['user'][0].first_name
        
        ##### start schedule #######
        
        data = pd.DataFrame(list(items),columns=['sfg_id','type_name','op_id_id','user_id','qty','date'])
        if len(data) != 0:
            # data = data.drop_duplicates()
            data.index = range(len(data))
            schedule_list = []
            # data['op_id'] = 0
            
            #change op from object to number (op_id)
            # for i in range(len(data)):
            #     data['op_id'][i] = data['op'][i].op_id
            sfg_list = data['sfg_id'].unique()
            data_total = data.pivot_table(index=['sfg_id'],columns=['op_id_id'],values=['qty'],aggfunc=np.sum)
            data_total.columns=data_total.columns.droplevel()
            data_total = data_total.fillna(0)
            data_total = round(data_total,2)
            for i in range(len(sfg_list)):
                # a = []
                # a.append(sfg_list[i])
                # a.append(data[data['sfg']==sfg_list[i]]['type'])
                # for j in range(len(all_op_id)):
                    
                #     user = data[(data['sfg']==sfg_list[i]) & (data['op_id']==all_op_id[j].op_id)]
                #     if not user.empty:
                #         a.append(user['user'][user.index[0]].last_name + user['user'][user.index[0]].first_name)
                #         a.append(user['date'][user.index[0]].strftime('%Y-%m-%d'))
                #     else:
                #         a.append('---')
                #         a.append('---')
                a={}
                a['sfg_id']= sfg_list[i]
                type = data[data['sfg_id']==sfg_list[i]]['type_name']
                a['type_name'] = type[type.index[0]]
                try:
                    sfg_comments = SfgComments.objects.get(sfg=a['sfg_id']).comments
                
                    a['sfg_comments'] = sfg_comments
                except:
                    a['sfg_comments'] = 'N'
                
                ####  test ########
                for j in range(len(all_op_id)):
                    user=  data[(data['sfg_id']==sfg_list[i]) & (data['op_id_id']==all_op_id[j].id)]
                    
                    if not user.empty:
                        username = User.objects.get(id=user['user_id'][user.index[0]]).get_full_name()
                        ###### get total qty
                        qty = data_total[data_total.index==sfg_list[i]][all_op_id[j].id]
                        # a[all_op_id[j].op_id] = username#user['user_id'][user.index[0]] + user['user_id'][user.index[0]]
                        # a[all_op_id[j].op_name] = user['date'][user.index[0]].strftime('%Y-%m-%d')
                        a[j+10] = username
                        a[j+100] =  user['date'][user.index[0]].strftime('%Y-%m-%d')
                        a[j+1000] = qty[0]
                       
                    else:
                        # a[all_op_id[j].op_id] = '---'
                        # a[all_op_id[j].op_name] = '---'
                        a[j+10] = '---'
                        a[j+100] = '---'
                        a[j+1000] = 0
                        

                schedule_list.append(a)
            # group = user_work_group(request)
            # all_user_ids = user_work_group_ids(group,date.today())

           
            

           

            #####数据组
            data_group, anls_result,anls_opcounts,sup_not_bor_total,sup_bor_total,over_time_total,data_opcounts = perform_analysis(request,user_groups,a_month,all_user_ids,all_op_id,a_year)
            if data_group:
                anls_group = data_group[0]
            else:
                anls_group = ''
            

            # end_time = time.time()

            if not is_manager and not is_electronic:
                group = user_work_group(request)
                all_user_ids = user_work_group_ids(group,today)
            
            p_perform_list, p_get_date,p_save_status = get_performance(request,all_user_ids, p_today)
            return render(request, 'report/schedule.html', {
                
                'schedule_list':schedule_list,
                'schedule_json':json.dumps(schedule_list),
                'op_list':all_op_id,
                
                'p_perform_list':p_perform_list,
                'p_date':p_get_date,
                'tab':tab,
                'anls_title':str(a_month)+'月份'+anls_group+'数据统计',
                'data_group':data_group,
                'test_a_month':a_month,
                'from_date':from_date,
                'to_date':to_date,
                'anls_result':anls_result.to_html(index=None),
                'p_save_status':p_save_status,
                # 'user_manager_group':user_manager_group,
                'anls_opcounts':anls_opcounts,
                'sup_not_bor_total':sup_not_bor_total.to_html(index=None),
                'sup_bor_total':sup_bor_total.to_html(),
                'over_time_total':over_time_total.to_html(),
                'user_groups':user_groups,  
            })
        else:
            return render(request, 'report/schedule.html',{
                'message':'It looks like no data between the select date'+work_group
            })
    else:
        f_user = User.objects.get(id=request.user.id)
        username = request.user.get_full_name()
        action_log = '访问'
        detail_message = '试图访问生产进度表'
        comments = 'Failed'
        query = TraceLog(user=f_user,username=username,action_log=action_log,detail_message=detail_message,comments=comments)
        query.save()
        # return HttpResponse('It looks like no group assigned for you or there are no users under your groups. Pleas contact admin')
        return render(request, 'report/schedule.html')


# 业绩表
def get_performance(request,all_users_id, today):
    p_get_date = today
    if not today:
        today = date.today()
        p_get_date = today.strftime('%Y-%m-%d')
    # user = User.objects.get(id=request.user.id)
    # groups = user.groups
    # forman_group=''
    # for i in groups.select_related():
    #     if '数据' in i.name:
    #         forman_group=i.name
    #         break
    check = is_report_manager(request)
    p_perform_list = []
    p_save_status='No'
    p_save_status_flag = GroupPerform.objects.filter(date=p_get_date,username__in=all_users_id)
    if(len(p_save_status_flag) >= len(all_users_id)):
        p_save_status='Yes'
    for i in range(len(all_users_id)):
        r_result = Report.objects.filter(user=all_users_id[i],date=today)
        produce_logs, standard_time_total, real_time_total = get_current_date_data(request, r_result)
        s_result = SupportiveTime.objects.filter(user=all_users_id[i],date=today)
        supportive_logs, supportive_total, supportive_total_without_coef, sup_total_without_coefBorrow,sup_total_without_borrow = get_supportive_history(request,s_result)
        a={}
        # performance module
        a['p_user'] = User.objects.get(id=all_users_id[i]).last_name + User.objects.get(id=all_users_id[i]).first_name
        a['p_standard'] =  round(standard_time_total,2)
        a['p_sup_without_borrow'] = sup_total_without_coefBorrow
        a['p_sup_borrow'] = round(supportive_total_without_coef-sup_total_without_coefBorrow,2)
        a['p_total'] = round(standard_time_total + supportive_total,2)
        a['p_real'] = round(real_time_total, 2)
        checkFlag = GroupPerform.objects.filter(date=p_get_date,username=all_users_id[i])
        if checkFlag:
            a['validate']='已保存'
           
        else:
            a['validate']='未保存'
        if real_time_total:
            a['p_kpi'] = round(standard_time_total/real_time_total,2) # 工效比
        else:
            a['p_kpi'] = 0
        if real_time_total or sup_total_without_coefBorrow:
            a['p_efficiency'] = round(real_time_total/(real_time_total+sup_total_without_coefBorrow),2) # 公式有效率
        else:
            a['p_efficiency'] = 0
        a['p_natural'] = round(real_time_total+supportive_total_without_coef, 2)
        # a['p_produce_log'] = produce_logs,
        # a['p_sup_log'] = supportive_logs,
        a['username'] = User.objects.get(id=all_users_id[i]).id
        # if check:
        gourp_user = User.objects.get(id=all_users_id[i]).groups
        for j in gourp_user.select_related():
            
            if '数据' in j.name:
                a['group'] = j.name
                break
        user_group = UserGroups.objects.get(user=all_users_id[i])
        a['work_group'] = user_group.work_group.group_name
        # else:
        #     a['group'] = forman_group
        
        p_perform_list.append(a)
    
    return p_perform_list, p_get_date, p_save_status

# 业绩表 popup
def perform_pop(request):
    date = request.GET.get('date')
    #return HttpResponse(date)
    # all_user_ids, all_op_id, user_groups = analysis_op_user(request)
    is_manager = is_report_manager(request)
    is_electronic = False
    orginal_group = get_groups(request)
    if any('班组长' and '电气' in word for word in orginal_group):
        is_electronic = True
    if is_manager or is_electronic:
        # manager can see all members
        all_user_ids, all_op_id,user_groups,all_work_groups = analysis_op_user(request)
    else:
        # forman can see only work group
        group = user_work_group(request)
        all_user_ids = user_work_group_ids(group,date)
    
    p_perform_list, p_get_date,p_save_status = get_performance(request,all_user_ids, date)

    return render(request, 'report/perform_pop.html', {
        'p_perform_list':p_perform_list,
        'p_date':p_get_date,
        'p_save_status':p_save_status,
        'all_user_ids':all_user_ids,
    })

###### return all op details and op count total
def getOpDetails(from_date,to_date,user_groups,all_op_id):
    
    results = Report.objects.filter(date__range=(from_date,to_date),groups__in=user_groups,op_id__in=all_op_id).values()
    df = pd.DataFrame(list(results), columns=['op_id_id','sfg_id','qty'])
    table = pd.pivot_table(df, index=['sfg_id'], columns=['op_id_id'], aggfunc=np.sum)
    table = table.round(2)
    data_opcounts = table[table==1]
    
   
    op_count_total = []
    #### swich op id to op name
    for i in range(len(data_opcounts.columns)):
        a={}
        op_name = Op.objects.get(id=data_opcounts.columns[i][1]).op_name
        qty = data_opcounts['qty'][data_opcounts.columns[i][1]].sum()
        a['op_name'] = op_name
        a['qty'] = qty
        op_count_total.append(a)
        data_opcounts = data_opcounts.rename(columns={data_opcounts.columns[i][1]:op_name})
    # data_opcounts = table.fillna(0)
    # data_opcounts=data_opcounts.fillna(0)
    # data_opcounts.columns = data_opcounts.columns.droplevel()
    # for i in range(len(data_opcounts.columns)):
    #     op_name = Op.objects.get(id=data_opcounts.columns[i]).op_name
    #     data_opcounts = data_opcounts.rename(columns={data_opcounts.columns[i]:op_name})

    ##### new code
    # data_opcounts = data_opcounts.fillna(0)
    # data_opcounts.index.name='SFG'
    # data_opcounts.columns.name = '工步'
    data_opcounts = table.fillna(0)
    
    for i in range(len(data_opcounts.columns)):
        op_name = Op.objects.get(id=data_opcounts.columns[i][1]).op_name
        data_opcounts = data_opcounts.rename(columns={data_opcounts.columns[i][1]:op_name,data_opcounts.columns[i][0]:'数量'})
    # data_opcounts.columns = data_opcounts.columns.droplevel()
    data_opcounts.index.name='SFG'

    return data_opcounts, op_count_total
###### return supportive time without borrow and borrow time in 统计表
def getSupportOpTime(from_date,to_date,user_groups):
    sup_logs = SupportiveTime.objects.filter(date__range=(from_date,to_date),groups__in=user_groups).values()
    sup_pd_data =  pd.DataFrame(list(sup_logs), columns=['user','rest','clean_time','inside_group','outside_group','complete_machine',
    'granite','prob','shortage','plan_change','human_quality_issue_rework','item_quality_issue','human_quality_issue_repair','equipment_mantainence',
    'inventory_check','quality_check','document','conference','group_management','record','vertical','borrow_time','borrow_name','comments','date'])
    sup_not_bor_total = sup_pd_data.sum()[1:21]
    sup_not_bor_total= sup_not_bor_total.to_frame()
    sup_not_bor_total = sup_not_bor_total.T.rename(columns={'rest':'休息','clean_time':'卫生','inside_group':'组内','outside_group':'组外','complete_machine':'整机',
    'granite':'花岗石','prob':'物流搬运','shortage':'补缺件','plan_change':'计划调整','human_quality_issue_rework':'人为质量问题',
    'item_quality_issue':'零件质量问题','human_quality_issue_repair':'人为质量问题返修','equipment_mantainence':'设备维护','inventory_check':'库存核查',
    'quality_check':'质量核查','document':'档案整理','conference':'会议','group_management':'班组管理','record':'记录','vertical':'线性/垂直度修正'})
    
    sup_bor_pd_data = sup_pd_data[['borrow_name','borrow_time']]
    sup_bor_total = sup_bor_pd_data.groupby(['borrow_name']).sum()
    sup_bor_total = sup_bor_total.rename(columns={'borrow_time':'外借工时'})
    sup_bor_total.index.name='外借种类'

    return sup_not_bor_total,sup_bor_total

#统计表 op_total
def perform_analysis(request,user_groups,a_month,all_user_ids,all_op_id,a_year):
    data_groups = []
    for i in range(len(user_groups)):
        if '数据' in user_groups[i]:
            data_groups.append(user_groups[i])
    today = date.today()
    
    if a_year ==0:
        year = today.year
    else:
        year = a_year

    if a_month != 0:
        m_range=monthrange(year,a_month)
        from_date = today.replace(year=year,month=a_month,day=1)
        to_date = today.replace(year=year,month=a_month, day=m_range[1])
    else:
        #return HttpResponse('a_month is 0')
        from_date = today.replace(year=year, month=1,day=1)
        to_date = today.replace(year=year,month=12,day=31)
        a_month='全年'
    
 
    
    # Get performance of person accroding to original group
    results = GroupPerform.objects.filter(date__range=(from_date,to_date),username__in=all_user_ids).values()
    df = pd.DataFrame(list(results), columns=['user','natural_time','performance','standard_time','real_time',
    'supportive_time','borrow_time','date','username','group'])
    # data = df.groupby(['user']).sum() # Group all users performance per
    if len(df) != 0:
        data = pd.pivot_table(df, index=['user'],values=['natural_time','performance','standard_time','real_time',
        'supportive_time','borrow_time'], aggfunc=np.sum) #{'natural_time':np.sum,'performance':np.sum,'standard_time':np.sum,'real_time':np.sum,
        # 'supportive_time':np.sum,'borrow_time':np.sum,'kpi':np.mean,'efficiency':np.mean})
        cols = ['natural_time','performance','standard_time','real_time',
        'supportive_time','borrow_time','kpi','efficiency']
        data.index.name='用户'
        data['kpi']=round(data['standard_time']/data['real_time'],2)
        data['efficiency']=round(data['real_time']/(data['real_time'] + data['supportive_time']),2)
        data = data[cols]
        
        total = data.sum()
        
        total.name = '总和'
        mean_kpi = round(total['standard_time']/total['real_time'],2)
        # data_efficiency = data[data['efficiency' ]!=0]
        # data_kpi = data[data['kpi'] !=0]
        
        mean_efficiency = round(total['real_time']/(total['real_time'] + total['supportive_time']),2)
        total['kpi'] = round(mean_kpi,2)
        total['efficiency'] = round(mean_efficiency,2)
        
        data = data.append(total)
    else:
        a = {'natural_time':[0,0],'performance':[0,0],'standard_time':[0,0],'real_time':[0,0],
        'supportive_time':[0,0],'borrow_time':[0,0],'kpi':[0,0],'efficiency':[0,0]}
        data = pd.DataFrame(data=a,index=['数据','汇总'])
    # data total for each person performance
    data.index.name='用户'
    data = data.rename(columns={"natural_time": "工作时间", "performance": "个人绩效", "standard_time": "标准工时", "real_time": "制造工时",
     "supportive_time":"辅助工时", "borrow_time": "外借工时", "kpi": "工效比","efficiency": "工时有效率"})
    data['年休假'] = 0
    data['调休假'] = 0
    results_leave = AnnualLeave.objects.filter(start_date__range=(from_date,to_date)).values()
    pd_leave = pd.DataFrame(list(results_leave),columns=['user','hours','leave_type'])
    pd_leave_total = pd.pivot_table(pd_leave,index=['user'],values=['hours'],columns=['leave_type'],aggfunc=np.sum)
    
    for i in range(len(data)):
        try:
            a = pd_leave_total[pd_leave_total.index==data.index[i]]
            try:
                data['年休假'][i] = a['hours']['年休假'][0]
            except:
                pass
            try:
                data['调休假'][i] = a['hours']['调休假'][0]
            except:
                pass
        except:
            pass
    

    # get annual leave time
    data = data.fillna(0.0)
    data = data.reset_index()
    # data=data.append(data.sum(numeric_only=True), ignore_index=True)
    # data_total = data.sum(numeric_only=True)

    # get all total qty based on ops


    #### old result ###
    # results = Report.objects.filter(date__range=(from_date,to_date),user__in=all_user_ids,op_id__in=all_op_id).values()

    # results = Report.objects.filter(date__range=(from_date,to_date),groups__in=user_groups,op_id__in=all_op_id).values()
    # df = pd.DataFrame(list(results), columns=['op_id_id','sfg_id','qty'])
    # table = pd.pivot_table(df, index=['sfg_id'], columns=['op_id_id'], aggfunc=np.sum)
    # table = table.round(2)
    # data_opcounts = table[table==1]
    data_opcounts,op_count_total = getOpDetails(from_date,to_date,user_groups,all_op_id)
   
    # op_count_total = []
    # #### swich op id to op name
    # for i in range(len(data_opcounts.columns)):
    #     a={}
    #     op_name = Op.objects.get(id=data_opcounts.columns[i][1]).op_name
    #     qty = data_opcounts['qty'][data_opcounts.columns[i][1]].sum()
    #     a['op_name'] = op_name
    #     a['qty'] = qty
    #     op_count_total.append(a)
    #     data_opcounts = data_opcounts.rename(columns={data_opcounts.columns[i][1]:op_name})
    # # data_opcounts = table.fillna(0)
    # # data_opcounts=data_opcounts.fillna(0)
    # # data_opcounts.columns = data_opcounts.columns.droplevel()
    # # for i in range(len(data_opcounts.columns)):
    # #     op_name = Op.objects.get(id=data_opcounts.columns[i]).op_name
    # #     data_opcounts = data_opcounts.rename(columns={data_opcounts.columns[i]:op_name})

    # ##### new code
    # # data_opcounts = data_opcounts.fillna(0)
    # # data_opcounts.index.name='SFG'
    # # data_opcounts.columns.name = '工步'
    # data_opcounts = table.fillna(0)
    
    # for i in range(len(data_opcounts.columns)):
    #     op_name = Op.objects.get(id=data_opcounts.columns[i][1]).op_name
    #     data_opcounts = data_opcounts.rename(columns={data_opcounts.columns[i][1]:op_name,data_opcounts.columns[i][0]:'数量'})
    # # data_opcounts.columns = data_opcounts.columns.droplevel()
    # data_opcounts.index.name='SFG'
    
    # supportive time analyze
    sup_not_bor_total,sup_bor_total = getSupportOpTime(from_date,to_date,user_groups)

    ### old code
    # sup_logs = SupportiveTime.objects.filter(date__range=(from_date,to_date),user__in=all_user_ids).values()
    # sup_logs = SupportiveTime.objects.filter(date__range=(from_date,to_date),groups__in=user_groups).values()
    # sup_pd_data =  pd.DataFrame(list(sup_logs), columns=['user','rest','clean_time','inside_group','outside_group','complete_machine',
    # 'granite','prob','shortage','plan_change','human_quality_issue_rework','item_quality_issue','human_quality_issue_repair','equipment_mantainence',
    # 'inventory_check','quality_check','document','conference','group_management','record','vertical','borrow_time','borrow_name','comments','date'])
    # sup_not_bor_total = sup_pd_data.sum()[1:21]
    # sup_not_bor_total= sup_not_bor_total.to_frame()
    # sup_not_bor_total = sup_not_bor_total.T.rename(columns={'rest':'休息','clean_time':'卫生','inside_group':'组内','outside_group':'组外','complete_machine':'整机',
    # 'granite':'花岗石','prob':'物流搬运','shortage':'补缺件','plan_change':'计划调整','human_quality_issue_rework':'人为质量问题',
    # 'item_quality_issue':'零件质量问题','human_quality_issue_repair':'人为质量问题返修','equipment_mantainence':'设备维护','inventory_check':'库存核查',
    # 'quality_check':'质量核查','document':'档案整理','conference':'会议','group_management':'班组管理','record':'记录','vertical':'线性/垂直度修正'})
    
    # sup_bor_pd_data = sup_pd_data[['borrow_name','borrow_time']]
    # sup_bor_total = sup_bor_pd_data.groupby(['borrow_name']).sum()
    # sup_bor_total = sup_bor_total.rename(columns={'borrow_time':'外借工时'})
    # sup_bor_total.index.name='外借种类'
################

    # over_time_data = Report.objects.filter(date__range=(from_date,to_date),user__in=all_user_ids).values_list('over_time','over_time_type')
    # over_time_data = OverTime.objects.filter(date__range=(from_date,to_date),groups__in=user_groups).values()
    # over_time_data = pd.DataFrame(list(over_time_data), columns=['user_id','over_time','over_time_type'])
    # over_time_total = over_time_data.groupby(['user_id']).sum()
    # over_time_total = over_time_total.rename(columns={'over_time':'加班工时'})
    # over_user=[]
    # for i in range(len(over_time_total)):
    #     user=User.objects.get(id=over_time_total.index[i]).get_full_name()
    #     over_user.append(user)
    # over_time_total.index=over_user

    ######## get over time total 
    over_time_total = getOverTime(from_date,to_date,user_groups)
    return data_groups, data, op_count_total, sup_not_bor_total,sup_bor_total,over_time_total,data_opcounts

######## return overtime total
def getOverTime(from_date,to_date,user_groups):
    over_time_data = OverTime.objects.filter(date__range=(from_date,to_date),groups__in=user_groups).values()
    over_time_data = pd.DataFrame(list(over_time_data), columns=['user_id','over_time','over_time_type'])
    over_time_total = over_time_data.groupby(['user_id']).sum()
    over_time_total = over_time_total.rename(columns={'over_time':'加班工时'})
    over_user=[]
    for i in range(len(over_time_total)):
        user=User.objects.get(id=over_time_total.index[i]).get_full_name()
        over_user.append(user)
    over_time_total.index=over_user
    return over_time_total


##### get all completed op
def opCompletTable(from_date,today):
    # today = date.today()
    # from_date = today.replace(day=1)
    ###### get values
    result = Report.objects.filter(date__range=(from_date,today)).values()
    df = pd.DataFrame(list(result),columns=['sfg_id','op_id_id','qty'])
    table = pd.pivot_table(df,index=['sfg_id'],columns=['op_id_id'],aggfunc=np.sum)
    table = table.fillna(0)
    try:
        table.columns=table.columns.droplevel()
        table = table.round(2)
    except:
        table = ''
    
    return table

def updateEchartOp(table):
    if len(table) != 0:
        if 5 in table.columns:
            op51 = len(table[5][table[5]==1])
        else:
            op51 = 0
        if 16 in table.columns:
            op142 = len(table[16][table[16]==1])
        else:
            op142 = 0
        return op51,op142 
    else:
        return 0,0



### get opDetails
def opdetails(request):
    today = date.today()
    from_date = today.replace(day=1)
    table = opCompletTable(from_date,today)
    for i in range(len(table.columns)):
        op_name = Op.objects.get(id=table.columns[i]).op_name
        table = table.rename(columns={table.columns[i]:op_name})
    table.columns.name='工步'
    table.index.name='SFG'
    return render(request,'report/opdetails.html',{
        'table':table.to_html(),
    })


### get group performance accroding to work group and assign kpi to according group not default group
def workTimeAnalysis(group,month,year):
    today = date.today()
    if month and year:
        end_date = calendar.monthrange(year,month)
        
        from_date = today.replace(year=year,month=month,day=1)
        to_date = today.replace(year=year,month=month,day=end_date[1])
    else:
        a = {'数据':[0,0]}
        data = pd.DataFrame(data=a)
    if month == 0:
        from_date = today.replace(year=year,month=1,day=1)
        to_date = today.replace(year=year,month=12,day=31)
    
    results = GroupPerform.objects.filter(work_group=group,date__range=(from_date,to_date)).values()
    df = pd.DataFrame(list(results), columns=['user','natural_time','performance','standard_time','real_time',
    'supportive_time','borrow_time','date','username','group'])
    # data = df.groupby(['user']).sum() # Group all users performance per
    if len(df) != 0:
        data = pd.pivot_table(df, index=['user'],values=['natural_time','performance','standard_time','real_time',
        'supportive_time','borrow_time'], aggfunc=np.sum) #{'natural_time':np.sum,'performance':np.sum,'standard_time':np.sum,'real_time':np.sum,
        # 'supportive_time':np.sum,'borrow_time':np.sum,'kpi':np.mean,'efficiency':np.mean})
        cols = ['natural_time','performance','standard_time','real_time',
        'supportive_time','borrow_time','kpi','efficiency']
        data.index.name='用户'
        data['kpi']=round(data['standard_time']/data['real_time'],2)
        data['efficiency']=round(data['real_time']/(data['real_time'] + data['supportive_time']),2)
        data = data[cols]
        
        total = data.sum()
        
        total.name = '总和'
        mean_kpi = round(total['standard_time']/total['real_time'],2)
        # data_efficiency = data[data['efficiency' ]!=0]
        # data_kpi = data[data['kpi'] !=0]
        
        mean_efficiency = round(total['real_time']/(total['real_time'] + total['supportive_time']),2)
        total['kpi'] = round(mean_kpi,2)
        total['efficiency'] = round(mean_efficiency,2)
        
        data = data.append(total)
        data = data.fillna(0.0)
        data = data.reset_index()
    else:
        a = {'natural_time':[0,0],'performance':[0,0],'standard_time':[0,0],'real_time':[0,0],
        'supportive_time':[0,0],'borrow_time':[0,0],'kpi':[0,0],'efficiency':[0,0]}
        data = pd.DataFrame(data=a,index=['数据','汇总'])
    # data total for each person performance
    
    data = data.rename(columns={"natural_time": "工作时间", "performance": "个人绩效", "standard_time": "标准工时", "real_time": "制造工时",
    "supportive_time":"辅助工时", "borrow_time": "外借工时", "kpi": "工效比","efficiency": "工时有效率"})
        
        
    return data

# get popup window in 统计表
def group_statistic(request):
    year = request.GET.get('year')
    month = request.GET.get('date')
    groups = request.GET.get('group')
    user = User.objects.get(id=request.user.id)
    require_user_groups = user.groups
   ### check if the use has the group 
    pemsion_check = False
    for i in require_user_groups.select_related():
        if groups in i.name:
            pemsion_check = True
            break
    
    check = is_report_manager(request)
    if pemsion_check or check:
        user_group=[groups]
        today = date.today()
        if not month:
            month=today.month
    
        else:        
            month = int(month)
        if not year:
            year = today.year
        else:
            year = int(year)
        if groups != 'ALL':
            ops = GroupOp.objects.filter(group_name=groups)

            all_users = User.objects.filter(groups__name=groups)
            all_user_ids = []
            all_op_id = []
            for i in range(len(all_users)):
                all_user_ids.append(all_users[i].id)
            for i in range(len(ops)):
                all_op_id.append(ops[i].op_id)
            # work_time_anls_group = user_work_group(request)
            work_time_anls = workTimeAnalysis(groups,month,year)
            work_time_anls_table = work_time_anls.to_html(index=None)
        else:
            all_user_ids, all_op_id, user_group,all_work_groups = analysis_op_user(request)
            a = {'数据':[0,0]}
            work_time_anls_table = pd.DataFrame(data=a).to_html(index=None)
             
            # return HttpResponse(all_user_ids)
        
        support_list = []
        for i in range(1,13):
            data_group, anls_result,anls_opcounts,sup_not_bor_total,sup_bor_total,over_time_total,data_opcounts = perform_analysis(request,user_group,i,all_user_ids,all_op_id,year)
            support_list.append(sup_not_bor_total)
        
        
        supp_bar = support_bar(support_list,month)
        # 王虎军
        if 11 in all_user_ids:
            all_user_ids.remove(11)
        # 王龙
        if 9 in all_user_ids:
            all_user_ids.remove(9)
        data_group, anls_result,anls_opcounts,sup_not_bor_total,sup_bor_total,over_time_total,data_opcounts = perform_analysis(request,user_group,month,all_user_ids,all_op_id,year)
        employee_bar = eply_kpi_bar(anls_result.drop(anls_result.index[len(anls_result)-1]))
        employee_eff_bar = eply_eff_bar(anls_result.drop(anls_result.index[len(anls_result)-1]))

        op_t_total = round(sup_not_bor_total.T.sum()[0],2)
        if check: 
            trans_time = getTransTime(request,month,year)
            trans_time=trans_time.to_html()

        else:
            trans_time=None
        oper_bar = op_bar(anls_opcounts)
        if month ==0:
            month = '全年'
        else:
            month = str(month)+'月'
        #### get group transfer time

        return render(request,'report/pop_analysis.html',{
            'anls_result':anls_result.to_html(index=None),
            'title':month+groups+'工时汇总',
            # 'op':all_op_id,
            # 'all_user_ids':all_user_ids,
            'anls_opcounts':anls_opcounts,
            'sup_not_bor_total':sup_not_bor_total.to_html(index=None),
            'over_time_total':over_time_total.to_html(),
            'sup_bor_total':sup_bor_total.to_html(),
            'employee_bar':employee_bar,
            'employee_eff_bar':employee_eff_bar,
            'op_bar':oper_bar,
            'supp_bar':supp_bar,
            'trans_time':trans_time,
            'data_opcounts':data_opcounts.to_html(),
            'work_time_anls_table':work_time_anls_table,
            'op_t_total':op_t_total,
            
        })
    else:
        f_user = User.objects.get(id=request.user.id)
        username = request.user.get_full_name()
        action_log = '查看'
        detail_message = '试图查看' + groups +'数据'
        comments = 'Failed'
        query = TraceLog(user=f_user,username=username,action_log=action_log,detail_message=detail_message,comments=comments)
        query.save()
        return HttpResponse("Sorry, 您无权查看 '" + groups+"'的数据。 Suspicious attempt will be reported to Administrator!")

# get user's produce log pop windows in performance section 
def per_get_prod_log(request):
    username = request.GET.get('username')
    date = request.GET.get('date')
    user = request.GET.get('user')
    
    results = Report.objects.filter(user__id=username,date=date)
    sup_results = SupportiveTime.objects.filter(user__id=username,date=date)
    
    list_logs, standard_time_total, real_time_total = get_current_date_data(request, results)
    # return HttpResponse(json.dumps(prod_log), content_type='application/json')

    supportive_logs, supportive_total, supportive_total_without_coef, sup_total_without_coefBorrow,sup_total_without_borrow = get_supportive_history(request,sup_results)
    
    overtime_data,overtime_data_group,overtime_total = get_overtime(request, username, date,date)
    return render(request,'report/individual_report.html', {
        'individual_log':list_logs,
        'individual_sup_log':supportive_logs,
        'supportive_total_without_coef':round(supportive_total_without_coef,2),
        'user':user,
        'real_time_total':round(real_time_total,2),
        'overtime_data':overtime_data.to_html(index=False),
        'overtime_data_group':overtime_data_group,
        'overtime_total':overtime_total,
        
    } )

# get overtime table list in 报工平台
def get_overtime(request,usernames,from_date,to_date):
    if(isinstance(usernames,list)):
        results = OverTime.objects.filter(user_id__in=usernames,date__range=(from_date,to_date)).values()

    else:
        results = OverTime.objects.filter(user_id=usernames,date__range=(from_date,to_date)).values()
    overtime_data = pd.DataFrame(list(results),columns=['user_id','over_time','over_time_type','is_paid','date'])
    overtime_data_group = overtime_data.groupby(['user_id']).sum()
    overtime_total = overtime_data['over_time'].sum()
    if overtime_total:
        overtime_total = round(overtime_total,2)
    else:
        overtime_total = 0
    del overtime_data['user_id']
    total1=pd.Series([overtime_total,'---','---','汇总'],index=['over_time','over_time_type','is_paid','date'])
    total1.name='汇总'
    overtime_data = overtime_data.append(total1)
    overtime_data = overtime_data.rename(columns={'over_time':'加班','over_time_type':'加班种类','is_paid':'加班费','date':'日期'})
    
    
    
    

    return overtime_data,overtime_data_group,overtime_total

# get total left quantity of certain SFG
def get_real_time_estimate(request):
    sfg = request.GET.get('sfg')
    op = request.GET.get('op')
    if int(op) == 11:
        real_time = {'real_time_estimate': ''}
        return HttpResponse(json.dumps(real_time), content_type='application/json')
        
    result = Report.objects.filter(sfg_id=sfg)
    if len(result) == 0:
        real_time = {'real_time_estimate': 1}
        return HttpResponse(json.dumps(real_time), content_type='application/json')

    else:
        total = 0
        for i in range(len(result)):
            if result[i].op_id.op_id == int(op):
                total += result[i].qty
        real_time = {'real_time_estimate': round(1 - total,2)}
        return HttpResponse(json.dumps(real_time), content_type='application/json')

#get produce time filtered by time in report get
def get_produce_time_bytime(request):
    
    from_date = request.POST.get('prod_from_date')
    to_date = request.POST.get('prod_to_date')
    today = date.today()
    message_from = None
    message_to = None
    if not from_date:
        from_date = today
        message_from = '没有开始日期'
    if not to_date:
        to_date=today
        message_to = '没有截止日期'
    username = request.user.id
    overtime_data,overtime_data_group,overtime_total = get_overtime(request,username,from_date,to_date)
    result = Report.objects.filter(user=username,date__range=(from_date,to_date)).order_by('date')
    logs,standard_time_total, real_time_total = get_current_date_data(request,result)
    all_show_digts = global_context(request)
    # switch the new data
    all_show_digts['logs'] = logs
    all_show_digts['error_prod_from_date'] = message_from
    all_show_digts['error_prod_to_date'] = message_to
    all_show_digts['overtime_total']= overtime_total,
    all_show_digts['overtime_data']= overtime_data.to_html(),

    return render(request,'report/report_get.html', all_show_digts )

# get supportive time filtered by date
def get_support_time_log(request):
    from_date = request.POST.get('support_from_date')
    to_date = request.POST.get('support_to_date')
    today = date.today()
    message_from = None
    message_to = None
    if not from_date:
        from_date = today
        message_from = '没有开始日期'
    if not to_date:
        to_date=today
        message_to = '没有截止日期'
    username = request.user.id
    result = SupportiveTime.objects.filter(user=username,date__range=(from_date,to_date)).order_by('date')
    supportive_logs, standard_time_total, real_time_total,sup_total_without_coefBorrow,sup_total_without_borrow = get_supportive_history(request,result)
    all_show_digts = global_context(request)
    all_show_digts['supportive_logs'] = supportive_logs
    all_show_digts['error_sup_from_date'] = message_from
    all_show_digts['error_sup_to_date'] = message_to

    return render(request,'report/report_get.html', all_show_digts )

# foreman save user performance day by day
def save_indiv_perform(request):
    user = request.GET.get('user')
    natural_time = request.GET.get('natural_time')
    perfom = request.GET.get('perfom')
    standard = request.GET.get('standard')
    real = request.GET.get('real')
    support = request.GET.get('support')
    borrow = request.GET.get('borrow')
    kpi = request.GET.get('kpi')
    efficiency = request.GET.get('efficiency')
    date = request.GET.get('date')
    username = request.GET.get('username')
    group = request.GET.get('group')
    work_group = request.GET.get('work_group')
    validate = request.GET.get('validate')
    checkFlag = GroupPerform.objects.filter(date=date,username=username)
    if validate =='未保存' and not checkFlag:
        query = GroupPerform(user=user,natural_time=natural_time,performance=perfom,standard_time=standard,real_time=real,supportive_time=support,
        borrow_time=borrow,kpi=kpi,efficiency=efficiency,date=date,username=username,group=group,work_group=work_group)
        try:
            query.save()
            message = user+'保存成功'
        except:
            message = user+'保存失败'

        return HttpResponse(json.dumps(message), content_type='application/json')
    else:
        message = user + '保存失败'
        return HttpResponse(json.dumps(message), content_type='application/json')

# Get comments of sfg for wang
def get_sfg_comments(request):
    sfg = request.GET.get('sfg')
    if not sfg:
        message = "没有找到SFG,请选中"


        return render(request, 'report/new_sfg_comments.html',{'message':message})
    
    else:
        try:
            results = SfgComments.objects.get(sfg=sfg)
        except:
            message = "无SFG备注信息，请创建"
            return render(request, 'report/new_sfg_comments.html',{'message':message,'sfg':sfg})
        if results:
            message = 'SFG备注信息'
            return render(request, 'report/update_sfg_comments.html',{
                'message':message,
                'sfg':sfg,
                'comments':results.comments
                })
        else:
            message = "无SFG备注信息，请创建"
            return render(request, 'report/new_sfg_comments.html',{'message':message,'sfg':sfg})

# create comments of sfg for wang
def create_new_sfg_comments(request):
    sfg = request.GET.get('sfg')
    comments = request.GET.get('comments')

    if sfg and comments:
        query = SfgComments(sfg=sfg,comments=comments)
        query.save()
        message='保存成功'

        return render(request, 'report/update_sfg_comments.html',{
                'save_message':message,
                'sfg':sfg,
                'comments':comments,
                })
    else:
        return render(request, 'report/update_sfg_comments.html',{
                'save_message':'没有填写备注信息',
                
                })

# update comments of sfg for wang
def update_sfg_comments(request):
    sfg = request.GET.get('sfg')
    comments = request.GET.get('comments')

    if sfg or comments:
        query = SfgComments.objects.get(sfg=sfg)
        query.comments=comments
        query.save()
        message='保存成功'

        return render(request, 'report/update_sfg_comments.html',{
                'save_message':message,
                'sfg':sfg,
                'comments':comments
                })
    else:
        return render(request, 'report/update_sfg_comments.html',{
                'save_message':'没有填写备注信息',
                
                })

### create docinfo record#####
def create_docinfo(request):
    doc_type=DocType.objects.all().values()
    js_doc_types = []
    for i in range(len(doc_type)):
        js_doc_types.append(doc_type[i]['type_id'])
    return render(request, 'report/create_docinfo.html',
    {
        'doc_type':doc_type,
        'js_doc_types':js_doc_types,
    })
    
######### Save doc Info #####
def save_doc_info(request):
    doc_type = DocType.objects.all().values()
    result=True
    sfg = request.GET.get('sfg')
    if not sfg:
        return HttpResponse('SFG 没有输入！请刷新网页，重新输入！')
    for i in range(len(doc_type)):
        data = request.GET.get(doc_type[i]['type_id'])
        type = DocType.objects.get(type=doc_type[i]['type'])
        old_data = DocInfo.objects.filter(sfg=sfg,type=type)
        if not data:
            data=' '
        if len(old_data) ==0:
            try:
                query = DocInfo(sfg=sfg,type=type,info=data)
                query.save()
            except Exception as ex:
                message = "保存失败： " + json.dumps(ex.args)
                result = False
                break
        else:
            # return HttpResponse(data)
            try:
                pre_data = DocInfo.objects.get(sfg=sfg,type=type)
                pre_data.info=data
                pre_data.save()
            except Exception as ex:
                message = "保存失败1 ： " + json.dumps(ex.args)
                result = False
                break
    
    if result:
        message = '保存成功！'

    return HttpResponse(json.dumps(message), content_type='application/json')

######### Search doc Info by date #####
def search_docinfo(request):
    # from_date = request.GET.get('from_date')
    # to_date = request.GET.get('to_date')
    sfg = request.GET.get('sfg')
    result = DocInfo.objects.filter(sfg__contains=sfg).values()
    #### Doc info df ####
    df_docinfo = pd.DataFrame(list(result),columns=['sfg','type_id','info'])
    doc_type_result = DocType.objects.all().values()
    ####### Doc Type df #####
    df_type = pd.DataFrame(list(doc_type_result),columns=['id','type'])
    
    doc_id = df_docinfo['sfg'].unique()
    doc_id = doc_id.tolist()
    
    return render(request, 'report/search_docinfo.html',{
        # 'from_date':from_date,
        # 'to_date':to_date,
        'result':df_docinfo.to_json(),
        'doc_type_result':df_type.to_json(),
        'doc_id':json.dumps(doc_id),
    })

###### Update Doc Info######
def update_docinfo(request):
    sfg = request.GET.get('sfg')

    doc_type=DocType.objects.all().values()
    doc_types = []
    doc_info = []
    for i in range(len(doc_type)):
        info_result = DocInfo.objects.filter(sfg=sfg,type=doc_type[i]['id']).values()
        a = {}
        a['type']= doc_type[i]['type']
        a['id'] = doc_type[i]['type_id']
        if len(info_result) != 0:
         
            a['info'] = info_result[0]['info']

        else:
            a['info']=' '
        doc_info.append(a)

    return render(request,'report/update_docinfo.html',{
        'doc_info':doc_info,
        'doc_type':doc_type,
        'sfg':sfg,


    })

###  show dashboard for different group ###########
@login_required(login_url='/accounts/login/')  
def dashBoard(request):
    all_user=['testa','testb','testp','testsm','teste','admin']
    if request.user.username in all_user:
        today = date.today()
        year = today.year
        month = today.month
        user = UserGroups.objects.get(user=request.user.id)
        group = user.work_group.group_name
        all_ids = workGroupId('数据-装配组A')
        all_user_ids, all_op_id, user_groups,all_work_groups = analysis_op_user(request)
        data_group, anls_result,anls_opcounts,sup_not_bor_total,sup_bor_total,over_time_total,data_opcounts = perform_analysis(request,group,month,all_ids,all_op_id,year)
        employee_bar = eply_kpi_bar(anls_result.drop(anls_result.index[len(anls_result)-1]))
        employee_eff_bar = eply_eff_bar(anls_result.drop(anls_result.index[len(anls_result)-1]))
        # perform = standardTime(anls_result.drop(anls_result.index[len(anls_result.index)-1]),anls_opcounts)
        oper_bar = op_bar(anls_opcounts)
        return render(request,'report/dashboard.html',{
            'employee_bar':employee_bar,
            'employee_eff_bar':employee_eff_bar,
            'oper_bar':oper_bar,
            # 'perform':perform,

        })
    else:
        return HttpResponse('You do not have permission to view it. Please contact admin')
    
### get temporary transfer of employees
@login_required(login_url='/accounts/login/')  
def getTransTime(request, month, year):
    if month == 0:
        today = date.today()
        from_date = today.replace(year=int(year),month=1,day=1)
        to_date = today.replace(year=int(year),month=12,day=31)
    else:
        today = date.today()
        date_range=monthrange(int(year),int(month))
        from_date = today.replace(year=int(year),month=int(month),day=1)
        to_date = today.replace(year=int(year),month=int(month),day=date_range[1])
    res = GroupPerform.objects.filter(date__range=(from_date,to_date)).values_list('group','work_group','natural_time')
    df = pd.DataFrame(list(res))
    if len(df) !=0:
        data = df[df[0]!=df[1]]
        piv = pd.pivot_table(data,index=0,columns=1,aggfunc=np.sum)
        piv.columns = piv.columns.droplevel()
        piv = piv.fillna(0)
        piv.columns.name='借调班组'
        piv.index.name='原班组'
        return piv
    else:
        return pd.DataFrame()

# approve material
def materialApprove(request):
    year = int(request.GET.get('year'))
    quarter = request.GET.get('quarter')
    group = request.GET.get('group')
    save_message = request.GET.get('messages')
    if not save_message:
        save_message=''
    if group != 'ALL':
        workGroup = WorkGroups.objects.get(group_name=group)
    matrl = Material.objects.all().values()
    matrl_pd = pd.DataFrame(list(matrl))
    is_manager = is_report_manager(request)
    if quarter != '0' and group != 'ALL':
        matrlApprove = MaterialApprove.objects.filter(year=year,quarter=quarter,group=workGroup).values()
        mSup = MeterialSurplus.objects.filter(group=workGroup).values()
    elif quarter !='0' and group == 'ALL':
        matrlApprove = MaterialApprove.objects.filter(year=year,quarter=quarter).values()
        mSup = MeterialSurplus.objects.all().values()
    elif quarter == '0' and group != 'ALL':
        matrlApprove = MaterialApprove.objects.filter(year=year,group=workGroup).values()
        mSup = MeterialSurplus.objects.filter(group=workGroup).values()
    else:
        matrlApprove = MaterialApprove.objects.filter(year=year).values()
        mSup = MeterialSurplus.objects.all().values()
    if len(mSup) != 0:
        mSup_pd = pd.DataFrame(list(mSup),columns=['sno_id','qty'])
        mSup_pd = mSup_pd.rename(columns={'qty':'qty_sup'})
        mSup_pd = mSup_pd.groupby('sno_id').sum()
    else:
        matrl_pd['qty_sup'] = 0
    if len(matrlApprove) ==0 and len(mSup) != 0:
        matrl_pd['qty_request'] = 0
        matrl_pd['qty'] = 0
        matrl_pd['total'] = matrl_pd.price * matrl_pd.qty_request
        matrl_pd = matrl_pd.merge(mSup_pd,left_on='id',right_on='sno_id',right_index=False,how='left')
    elif len(matrlApprove)==0 and len(mSup) == 0:
        matrl_pd['qty_sup'] = 0
    else:
        mAppro_pd = pd.DataFrame(list(matrlApprove),columns=['sno_id','qty','qty_request'])
        mAppro_pd = mAppro_pd.groupby('sno_id').sum()
        # data = pd.merge(matrl_pd, mAppro_pd.set_index('sno_id'),left_on='id',right_index=True)
        matrl_pd = matrl_pd.merge(mAppro_pd,left_on='id',right_on=mAppro_pd.index,right_index=False,how='left')
        if len(mSup) != 0:
            matrl_pd = matrl_pd.merge(mSup_pd,left_on='id',right_on='sno_id',right_index=False,how='left')
        # matrl_pd = matrl_pd.merge(mAppro_pd.set_index('sno_id'),left_on='id',right_index=True)
        matrl_pd['total'] = matrl_pd.price * matrl_pd.qty_request
    # matrlUse = MeterialUse.objects.filter()
    mapprove_data = matrl_pd.to_json(orient='records',lines=True)
    mapprove_data = mapprove_data.split('\n')
    if quarter == '0':
        quarter = '全年'
    return render(request, 'report/material_approve.html',{
        'year':year,
        'quarter':quarter,
        'group':group,
        'matrl':matrl_pd.to_json(orient='records'),
        # 'mapprove_data':matrl_pd.to_html(index=False),
        'is_manager':is_manager,
        'save_message':save_message,

    })

# get material
def materialGet(request):
    year = request.GET.get('year')
    quarter = request.GET.get('quarter')
    group = request.GET.get('group')
    if group != 'ALL':
        workGroup = WorkGroups.objects.get(group_name=group)
    matrl = Material.objects.all().values()
    matrl_pd = pd.DataFrame(list(matrl))
    if quarter != '0' and group != 'ALL':
        matrlGet = MaterialApprove.objects.filter(year=year,quarter=quarter,group=workGroup).values()
    elif quarter != '0' and group == 'ALL':
        matrlGet = MaterialApprove.objects.filter(year=year,quarter=quarter).values()
    elif quarter == '0' and group != 'ALL':
        matrlGet = MaterialApprove.objects.filter(year=year,group=workGroup).values()
    else:
        matrlGet = MaterialApprove.objects.filter(year=year).values()   
    if len(matrlGet) ==0:
        matrl_pd['qty_get'] = 0
    else:
        mGet_pd = pd.DataFrame(list(matrlGet),columns=['sno_id','qty_get','qty'])
        mGet_pd = mGet_pd.groupby('sno_id').sum()
        matrl_pd = matrl_pd.merge(mGet_pd,left_on='id',right_on=mGet_pd.index,right_index=False,how='left')
        # matrl_pd = matrl_pd.merge(mGet_pd.set_index('sno_id'),left_on='id',right_index=True)
    if quarter == '0':
        quarter = '全年'
    return render(request,'report/material_get.html',{
        'matrl':matrl_pd.to_json(orient='records'),
        'year':year,
        'quarter':quarter,
        'group':group,
        })

# check material
def materialCheck(request):
    year = request.GET.get('year')
    quarter = request.GET.get('quarter')
    group = request.GET.get('group')
    matrl = Material.objects.all().values()
    matrl_pd = pd.DataFrame(list(matrl))
    if group != 'ALL':
        workGroup = WorkGroups.objects.get(group_name=group)
    if quarter != '0' and group != 'ALL':
        matrlApprove = MaterialApprove.objects.filter(year=year,quarter=quarter,group=workGroup).values()
        matrlUse = MeterialUse.objects.filter(year=year,quarter=quarter,group=workGroup).values()
        mSup = MeterialSurplus.objects.filter(group=workGroup).values()
    elif quarter != '0' and group == 'ALL':
        matrlApprove = MaterialApprove.objects.filter(year=year,quarter=quarter).values()
        matrlUse = MeterialUse.objects.filter(year=year,quarter=quarter).values()
        mSup = MeterialSurplus.objects.all().values()
    elif quarter == '0' and group != 'ALL':
        matrlApprove = MaterialApprove.objects.filter(year=year,group=workGroup).values()
        matrlUse = MeterialUse.objects.filter(year=year,group=workGroup).values()
        mSup = MeterialSurplus.objects.filter(group=workGroup).values()
    else:
        matrlApprove = MaterialApprove.objects.filter(year=year).values() 
        matrlUse = MeterialUse.objects.filter(year=year).values()
        mSup = MeterialSurplus.objects.all().values()

    # mSup = MeterialSurplus.objects.all().values()
    if len(mSup) != 0:
        mSup_pd = pd.DataFrame(list(mSup),columns=['sno_id','qty'])
        mSup_pd = mSup_pd.rename(columns={'qty':'qty_sup'})
        mSup_pd = mSup_pd.groupby('sno_id').sum()
    else:
        matrl_pd['qty_sup'] = 0
    # check if get is empty
    if len(matrlApprove)==0 and len(mSup) != 0:
        matrl_pd['qty'] = 0
        matrl_pd['qty_request'] = 0
        matrl_pd['qty_get'] = 0
        # matrl_pd['qty_sup'] = 0
        matrl_pd = matrl_pd.merge(mSup_pd,left_on='id',right_on='sno_id',right_index=False,how='left')
    elif len(matrlApprove)==0 and len(mSup) == 0:
        matrl_pd['qty_sup'] = 0
        matrl_pd['qty_get'] = 0
    else:
        mApp=pd.DataFrame(list(matrlApprove),columns=['sno_id','qty','qty_request','qty_get'])
        mApp = mApp.groupby('sno_id').sum()
        matrl_pd = matrl_pd.merge(mApp, left_on='id', right_on=mApp.index,right_index=False,how='left')
        if len(mSup) != 0:
            matrl_pd = matrl_pd.merge(mSup_pd,left_on='id',right_on='sno_id',right_index=False,how='left')

    if (len(matrlUse)==0):
        matrl_pd['qty_use']=0
    else:
        matrlUse_pd = pd.DataFrame(list(matrlUse),columns=['sno_id','qty'])
        matrlUse_pd = matrlUse_pd.rename(columns={'qty':'qty_use'})
        matrlUse_pd = matrlUse_pd.groupby('sno_id').sum()
        matrl_pd = matrl_pd.merge(matrlUse_pd, left_on='id',right_on=matrlUse_pd.index,right_index=False,how='left')

    matrl_pd = matrl_pd.fillna(0)
    matrl_pd['calc_left'] = matrl_pd.qty_get - matrl_pd.qty_use + matrl_pd.qty_sup
    if quarter=='0':
        quarter = '全年'
    return render(request,'report/material_check.html',{
        'matrl':matrl_pd.to_json(orient='records'),
        'year':year,
        'quarter':quarter,
        'group':group,
        })

def getMaterialNo(request):
    msno = request.GET.get('msno')
    msno = msno.strip()
    try:
        name = Material.objects.get(sno__contains=msno)
        fullName = name.name + ' ' +name.attribute
        
    except:
        fullName = '找不到物料'
    
    return HttpResponse(json.dumps(fullName), content_type='application/json')

def saveMaterialUse(request):
    sno = request.GET.get('msno')
    qty = request.GET.get('qty')
    try:
        f_sno = Material.objects.get(sno=sno)
        
        #qty = round(float(qty),2)
        today = date.today()
        year = today.year
        qauter=math.ceil(today.month/3)
        qauter = 'Q' +str(qauter)
        group = user_work_group(request)
        f_group = WorkGroups.objects.get(group_name=group)
        f_user = User.objects.get(id=request.user.id)
        query = MeterialUse(sno=f_sno,year=year,quarter=qauter,group=f_group,qty=qty,user=f_user)
        try:
            query.save()
            message = '保存成功'
        except:
            message = '保存不成功'
    except Exception as ex:    
        template = "保存失败，找不到物料编号"
        message = template + json.dumps(ex.args)
        
    
    return HttpResponse(json.dumps(message),content_type='application/json')

def saveMaterialApprove(request):
    ids = request.POST.getlist('ids')
    qtys = request.POST.getlist('qtys')
    quarter = request.POST.get('quarter')
    year = int(request.POST.get('year'))
    group = request.POST.get('group')
    is_manager = is_report_manager(request)
    not_in_list = []
    message = ''
    if quarter != '全年' and group != 'ALL':
        for i in range(len(ids)):
            f_id = Material.objects.get(sno=ids[i])
            f_group = WorkGroups.objects.get(group_name=group)
            user = User.objects.get(id=request.user.id)
            a = MaterialApprove.objects.filter(year=year,quarter=quarter,group=f_group,sno=f_id)
            if len(a) == 0:
                if is_manager and qtys[i] !=0:
                    query = MaterialApprove(year=year,quarter=quarter,group=f_group,sno=f_id,user=user,qty=qtys[i])
                    query.save()
                    message += ids[i] + '审批保存成功'
                else:
                    query = MaterialApprove(year=year,quarter=quarter,group=f_group,sno=f_id,user=user,qty_request=qtys[i])
                    query.save()  
                    message += ids[i] + '申请保存成功'              
            else:
                if is_manager and qtys[i] !=0:
                    a.update(qty=qtys[i])
                    message += ids[i] + '审批更新保存成功'
                else:
                    a.update(qty_request=qtys[i])
                    message += ids[i] + '申请更新保存成功'
    else:
        message = '请选择年份，季度和班组'

    return HttpResponse(json.dumps(message))

def saveMaterialGet(request):
    ids = request.POST.getlist('ids')
    qtys = request.POST.getlist('qtys')
    quarter = request.POST.get('quarter')
    year = int(request.POST.get('year'))
    group = request.POST.get('group')
    message = ''
    if quarter != '全年' and group != 'ALL':
        for i in range(len(ids)):
            f_id = Material.objects.get(sno=ids[i])
            f_group = WorkGroups.objects.get(group_name=group)
            user = User.objects.get(id=request.user.id)
            a = MaterialApprove.objects.filter(year=year,quarter=quarter,group=f_group,sno=f_id)
            if len(a) == 0:
                # query = MaterialGet(year=year,quarter=quarter,group=f_group,sno=f_id,user=user,qty=qtys[i])
                # query.save()
                message += ids[i] + '没有申请和审批流程,无法更新！'              
            else:
                a.update(qty_get=qtys[i])
                message += ids[i] + '到货更新保存成功'
    else:
        message = '请选择年份，季度和班组'
    return HttpResponse(json.dumps(message))

def saveMaterialSup(request):
    ids = request.POST.getlist('ids')
    qtys = request.POST.getlist('qtys')
    quarter = request.POST.get('quarter')
    year = int(request.POST.get('year'))
    group = request.POST.get('group')
    message = ''
    if quarter != '全年' and group != 'ALL':
        for i in range(len(ids)):
            f_id = Material.objects.get(sno=ids[i])
            f_group = WorkGroups.objects.get(group_name=group)
            user = User.objects.get(id=request.user.id)
            a = MeterialSurplus.objects.filter(group=f_group,sno=f_id)
            if len(a) == 0:
                query = MeterialSurplus(year=year,quarter=quarter,group=f_group,sno=f_id,user=user,qty=qtys[i])
                query.save()
                # message += ids[i] + '没有申请和审批流程,无法更新！'              
            else:
                a.update(qty=float(qtys[i]))
                message += ids[i] + '结余更新保存成功'
    else:
        message = '请选择年份，季度和班组'
    return HttpResponse(json.dumps(message))

def uploadMatrlAprv(request):
    message = []
    error = []
    if request.method == 'POST':
        excel_file = request.FILES["files"]
        data = pd.read_excel(excel_file)
        year = int(request.POST.get('year'))
        quarter = request.POST.get('quarter')
        group = request.POST.get('group')
        cols = data.columns[1:]
        f_user = User.objects.get(id=request.user.id)
        for i in range(len(data)):
            
            f_sno = Material.objects.get(sno=data['ID'][i])
            for j in range(len(cols)):
                f_group = WorkGroups.objects.get(group_name=cols[j])
                a = MaterialApprove.objects.filter(sno=f_sno,year=year,quarter=quarter,group=f_group)
                if len(a) != 0:
                    try:
                        a.update(qty=int(data[cols[j]][i]))
                        message.append('保存成功')
                    except Exception as ex:
                        error.append(json.dumps(ex.args))

                else:
                    try:
                        query = MaterialApprove(sno=f_sno,year=year,quarter=quarter,group=f_group,user=f_user,qty=int(data[cols[j]][i]))
                        query.save()
                        message.append('保存成功')
                    except Exception as ex:
                        error.append(str(data['ID'][i])+',group:' + cols[j] + '没有保存，因为没有申请数据。')
        # message = list(set(message))
        if len(error) != 0:
            messages = str(len(message))+'条保存成功'+str(len(error))+'条保存失败'
        else:
            messages = str(len(message))+'条保存成功'

    return HttpResponseRedirect('/report/materialApprove/?year='+str(year)+'&quarter='+quarter+"&group="+group+"&messages= "+str(messages))
    # return HttpResponse(message)

