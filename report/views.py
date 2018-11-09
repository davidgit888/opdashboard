from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Prob, Op, SfmProd, TypeStandard, Report,SupportiveTime,CoefficientSupport,Borrow,GroupOp
from datetime import date
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
import json
from django.conf import settings as original_settings
from django.template import RequestContext
import pandas as pd

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
        a['date'] = result[i].date
        standard_time_total +=a['standard']
        real_time_total += a['real']
        quantity_total += a['qty']
        count_total += 1
        list_logs.append(a)
    a={}
    a['sfg'] = '汇总'
    a['type'] = count_total
    a['op'] = count_total
    a['prob'] = '---'
    a['standard'] = standard_time_total
    a['real'] = real_time_total
    a['qty'] = quantity_total
    a['date'] = '---'
    list_logs.append(a)

    

    return list_logs, standard_time_total, real_time_total
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

    supportive_logs,supportive_total = get_supportive_history(request, reuslt_today_supportive)
    supportive_logs1,supportive_total1 = get_supportive_history(request, reuslt_month_supportive)
    supportive_logs2,supportive_total2 = get_supportive_history(request, reuslt_year_supportive)

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
    
    if real_time_total or supportive_total:
        efficiency_today = real_time_total/(real_time_total+supportive_total)
    else:
        efficiency_today=0
    if real_time_total1 or supportive_total1:
        efficiency_month = real_time_total1/(real_time_total1+supportive_total1)
    else:
        efficiency_month=0
    if real_time_total2 or supportive_total2:
        efficiency_year = real_time_total2/(real_time_total2+supportive_total2)
    else:
        efficiency_year=0

    borrow = Borrow.objects.all()

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
        'borrow_time':borrow,
        
        }

    return all_shown_digits

def get_supportive_history(request,result):
    supportive_logs=[]
    coef = CoefficientSupport.objects.all()

    list_total = [ [] for i in range(21)]
    for i in range(len(list_total)):
        list_total[i] = 0
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
        a['date'] = result[i].date
        a['borrow_time'] = result[i].borrow_time
        a['borrow_name'] = result[i].borrow_name
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
        list_total[19] += a['borrow_time'] * coef[0].borrow_time
        
        supportive_logs.append(a)
    list_total[20] = '汇总'
    a={}
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
    a['borrow_time'] = list_total[19]
    a['borrow_name'] = '---'
    a['date'] = list_total[20]
    supportive_total = 0
    for i in range(len(list_total)-1):
        supportive_total += list_total[i]
    supportive_logs.append(a)
     
    return supportive_logs, supportive_total

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
    ops = Op.objects.all()
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
    supportive_logs,supportive_total = get_supportive_history(request, reuslt_today_supportive)
    
    return probs, ops, group, history_logs, today_kpi, month_kpi, year_kpi,supportive_logs, supportive_total

# when load the page
@login_required(login_url='/accounts/login/')  
def index(request):
    # probs = Prob.objects.all()
    # ops = Op.objects.all()
    # groups = request.user.groups.all().values()
    # group=None
    # #get current username and report history for today
    # #today date
    # today = date.today()
    # month_first = today.replace(day=1) #first date of month
    # year_first = today.replace(day=1,month=1) #first date of year
    # username = request.user.id
    # # get data for KPI
    # result_today = Report.objects.filter(user=username, date=date.today())
    # result_this_month = Report.objects.filter(user=username,date__range=(month_first,today))
    # result_this_year = Report.objects.filter(user=username,date__range=(year_first,today))
    # history_logs = get_current_date_data(request,result_today)

    # # day kpi
    # real_time_today, stand_time_today = get_kpi(request,result_today)
    # if real_time_today and stand_time_today:
    #     today_kpi = round(stand_time_today/real_time_today,2)
    # else:
    #     today_kpi=0

    # real_time_month, stand_time_month = get_kpi(request, result_this_month)
    # if real_time_month and stand_time_month:
    #     month_kpi = round(stand_time_month/real_time_month,2)
    # else:
    #     month_kpi = 0

    # real_time_year, stand_time_year = get_kpi(request, result_this_year)
    # if real_time_year and stand_time_year:
    #     year_kpi = round(stand_time_year/real_time_year,2)
    # else:
    #     year_kpi=0
    # # check prob text box
    # for i in groups:
    #     if '检验组' in i['name']:
    #         group = 1
    # #save_message=request.POST('save_message')

    probs, ops, group, history_logs, today_kpi, month_kpi, year_kpi,supportive_logs,supportive_total = load_all_data(request)
    all_show_digts = global_context(request)

    local_jason = {
        'op_list':ops,
        'prob_list':probs,
        'groups':group,
        'logs':history_logs,
        'today_kpi':today_kpi,
        'month_kpi':month_kpi,
        'year_kpi':year_kpi,
        'supportive_logs':supportive_logs,
        'supportive_total':supportive_total,
        #'save_message':,
    }
    all_dict = local_jason.copy()
    all_dict.update(all_show_digts)
    return render(request, 'report/report_get.html', all_dict)

# when click submit to save to database
@login_required(login_url='/accounts/login/')  
def get_data(request):
    # probs = Prob.objects.all()
    # ops = Op.objects.all()
    # groups = request.user.groups.all().values()
    # username = request.user.id
    # result_today = Report.objects.filter(user=username, date=date.today())
    # history_logs = get_current_date_data(request,result_today)
    # group=None
    # for i in groups:
    #     if '检验组' in i['name']:
    #         group = 1
    sfg = request.POST['sfg_id']
    type = request.POST['type']
    op_id = request.POST['op_id']
    prob_info = request.POST['prob_info']
    user = request.POST['user_name']
    standard_time = request.POST['standard_time']
    real_time = request.POST['real_time']
    qty = request.POST['qty']
    date_time = request.POST.get('prodate')
    
    #load data
    
    if prob_info== 'None':
        prob_info=''
    if prob_info == '---':
        prob_info=None
    if prob_info == '空':
        prob_info=None

    

    try:
        #f_sfg = SfmProd.objects.get(sfg_id=sfg)
        f_op = Op.objects.get(op_id=op_id)
        f_user = User.objects.get(id=user)
        query = Report(sfg_id=sfg,type_name=type,op_id=f_op,prob=prob_info,qty=qty,user=f_user,standard_tiem=standard_time,real_time=real_time,date=date_time)
        query.save()
        probs, ops, group, history_logs, today_kpi, month_kpi, year_kpi,supportive_logs,supportive_total = load_all_data(request)
        all_show_digits = global_context(request)
        save_message="保存成功"
        local_jason = {
            'op_list':ops,
            'prob_list':probs,
            'groups':group,
            'logs':history_logs,
            'today_kpi':today_kpi,
            'month_kpi':month_kpi,
            'year_kpi':year_kpi,
            'save_message':save_message,
            'supportive_logs':supportive_logs,
            'supportive_total':supportive_total,

        }

        
        all_dict = local_jason.copy()
        all_dict.update(all_show_digits)


        return render(request, 'report/report_get.html', all_dict)
    except Exception as ex:    
        template = "保存失败"
        message = template + json.dumps(ex.args)
        probs, ops, group, history_logs, today_kpi, month_kpi, year_kpi, supportive_logs,supportive_total = load_all_data(request)
        all_show_digits = global_context(request)
        local_jason1 = {
            'op_list':ops,
            'prob_list':probs,
            'groups':group,
            'logs':history_logs,
            'today_kpi':today_kpi,
            'month_kpi':month_kpi,
            'year_kpi':year_kpi,
            'error_message':message,
            'supportive_logs':supportive_logs,
            'supportive_total':supportive_total,
         }
        
        
        all_dict1 = local_jason1.copy()
        all_dict1.update(all_show_digits)
        return render(request, 'report/report_get.html', all_dict1)
    
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

    rest = request.POST['rest']
    clean = request.POST['clean']
    record = request.POST['record']
    inside_group = request.POST['inside_group']
    outside_group = request.POST['outside_group']
    complete_machine = request.POST['complete_machine']
    granite = request.POST['granite']
    prob = request.POST['prob']
    shortage = request.POST['shortage']
    plan_change = request.POST['plan_change']
    human_quality_issue_rework = request.POST['human_quality_issue_rework']
    item_quality_issue = request.POST['item_quality_issue']
    human_quality_issue_repair = request.POST['human_quality_issue_repair']
    equipment_mantainence = request.POST['equipment_mantainence']
    inventory_check = request.POST['inventory_check']
    quality_check = request.POST['quality_check']
    document = request.POST['document']
    conference = request.POST['conference']
    group_management = request.POST['group_management']
    borrow_time = request.POST['borrow_time']
    borrow_type = request.POST['borrow_type']
    date_time = request.POST.get('suportdate')
    
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

    
    try:    

        f_user = User.objects.get(id=request.user.id)
        query = SupportiveTime(user=f_user,rest=rest,clean_time=clean,inside_group=inside_group,outside_group=outside_group,
        complete_machine=complete_machine,granite=granite,prob=prob,shortage=shortage,plan_change=plan_change,
        human_quality_issue_rework=human_quality_issue_rework,item_quality_issue=item_quality_issue,human_quality_issue_repair=human_quality_issue_repair,
        equipment_mantainence=equipment_mantainence,inventory_check=inventory_check,quality_check=quality_check,
        document=document,conference=conference,group_management=group_management,record=record,date=date_time,borrow_time=borrow_time,borrow_name=borrow_type)

        query.save()
        probs, ops, group, history_logs, today_kpi, month_kpi, year_kpi, supportive_logs,supportive_total = load_all_data(request)
        save_message="保存成功"
        all_show_digits = global_context(request)
        local_jason = {
            'op_list':ops,
            'prob_list':probs,
            'groups':group,
            'logs':history_logs,
            'today_kpi':today_kpi,
            'month_kpi':month_kpi,
            'year_kpi':year_kpi,
            'supportive_save_message':save_message,
            'supportive_logs':supportive_logs,
            'supportive_total':supportive_total,

        }
        all_dict = local_jason.copy()
        all_dict.update(all_show_digits)
        return render(request, 'report/report_get.html', all_dict)
    except Exception as ex:    
        template = "保存失败"
        message = template + json.dumps(ex.args)
        probs, ops, group, history_logs, today_kpi, month_kpi, year_kpi, supportive_logs,supportive_total = load_all_data(request)
        local_jason = {
            'op_list':ops,
            'prob_list':probs,
            'groups':group,
            'logs':history_logs,
            'today_kpi':today_kpi,
            'month_kpi':month_kpi,
            'year_kpi':year_kpi,
            'supportive_error_message':message,
            'supportive_logs':supportive_logs,
            'supportive_total':supportive_total,
         }
        all_show_digits = global_context(request)
        all_dict = local_jason.copy()
        all_dict.update(all_show_digits)
        return render(request, 'report/report_get.html', all_dict)
    


    # return render(request, 'report/report_get.html',{
    #     'save_message':"successful",
    #     'borrow':borrow_time,
    # })

@login_required(login_url='/accounts/login/')  
def get_sfgid(request):
    a = request.GET.get('a')
    try:
        type = SfmProd.objects.get(sfg_id=a).type_name
    except:
        type='找不到SFG ID'

    return_json = {'result':type}
    return HttpResponse(json.dumps(return_json), content_type='application/json')

@login_required(login_url='/accounts/login/')  
def get_standard_time(request):
    type = request.GET.get('type')
    op = request.GET.get('op')
    prob = request.GET.get('prob')
    qty = request.GET.get('qty')
    
    if prob == 'None':
        prob = None
        try:
            standart_time = TypeStandard.objects.get(op_id=op,type_name=type,prob_info=prob).standard_time 
            standart_time = float(standart_time) * float(qty)
            result = {'result':standart_time}
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

def get_groups(request):
    user_all_permissions = []
    user = User.objects.get(id=request.user.id)
    groups = user.groups
    for i in groups.select_related():
        user_all_permissions.append(i.name)

    return user_all_permissions

# produce schedule table
def report_analysis(request):

    user_groups = get_groups(request)
    all_user_ids = []
    all_op_id = []
    #get all user belong to current user's groups
    for j in range(len(user_groups)):
        if '数据-装配组A' in user_groups[j]:
            users = User.objects.filter(groups__name='数据-装配组A')
            for i in range(len(users)):
                all_user_ids.append(users[i].id)

            ops = GroupOp.objects.filter(group_name='数据-装配组A')
            for i in range(len(ops)):
                all_op_id.append(ops[i].op_id)

        if '数据-装配组B' in user_groups[j]:
            users = User.objects.filter(groups__name='数据-装配组B')
            for i in range(len(users)):
                all_user_ids.append(users[i].id)

            ops = GroupOp.objects.filter(group_name='数据-装配组B')
            for i in range(len(ops)):
                all_op_id.append(ops[i].op_id)

        if '数据-电气' in user_groups[j]:
            users = User.objects.filter(groups__name='数据-电气')
            for i in range(len(users)):
                all_user_ids.append(users[i].id)

            ops = GroupOp.objects.filter(group_name='数据-电气')
            for i in range(len(ops)):
                all_op_id.append(ops[i].op_id)

        if '数据-包装' in user_groups[j]:
            users = User.objects.filter(groups__name='数据-包装')
            for i in range(len(users)):
                all_user_ids.append(users[i].id)
            
            ops = GroupOp.objects.filter(group_name='数据-包装')
            for i in range(len(ops)):
                all_op_id.append(ops[i].op_id)
        

    # get Op name
    
    op_list = []
    all_user_ids = list(set(all_user_ids))
    all_op_id = list(set(all_op_id))
    
    if len(all_user_ids) != 0 and len(all_op_id) != 0:
        items = Report.objects.filter(user_id__in=all_user_ids).filter(op_id__in=all_op_id).order_by('date')
        #data = pd.DataFrame(list(items), columns=['sfg_id','type_name','op_id_id','user_id','date'])
        data = pd.DataFrame()
        for i in range(len(items)):
            data = data.append({'sfg':items[i].sfg_id, 'type':items[i].type_name,'op':items[i].op_id,'user':items[i].user,'date':items[i].date}, ignore_index=True)
            # data['op'][0].op_id
            # data['user'][0].last_name
            # data['user'][0].first_name
        data = data.drop_duplicates()
        data.index = range(len(data))
        schedule_list = []
        data['op_id'] = 0
        for i in range(len(data)):
            data['op_id'][i] = data['op'][i].op_id
        sfg_list = data['sfg'].unique()

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
            a['sfg']= sfg_list[i]
            type = data[data['sfg']==sfg_list[i]]['type']
            a['type'] = type[type.index[0]]

            ####  test ########
            for j in range(len(all_op_id)):
                user=  data[(data['sfg']==sfg_list[i]) & (data['op_id']==all_op_id[j].op_id)]

                if not user.empty:
                    a[all_op_id[j].op_id] = user['user'][user.index[0]].last_name + user['user'][user.index[0]].first_name
                    a[all_op_id[j].op_name] = user['date'][user.index[0]].strftime('%Y-%m-%d')
                else:
                    a[all_op_id[j].op_id] = '---'
                    a[all_op_id[j].op_name] = '---'
            #############
            # #####11
            # user=  data[(data['sfg']==sfg_list[i]) & (data['op_id']==11)]
            # if not user.empty:
            #     a['user11'] = user['user'][user.index[0]].last_name + user['user'][user.index[0]].first_name
            #     a['data11'] = user['date'][user.index[0]].strftime('%Y-%m-%d')
            # else:
            #     a['user11'] = '--'
            #     a['data11'] = '--'
            # #### 21
            # user=  data[(data['sfg']==sfg_list[i]) & (data['op_id']==21)]
            # if not user.empty:
            #     a['user21'] = user['user'][user.index[0]].last_name + user['user'][user.index[0]].first_name
            #     a['data21'] = user['date'][user.index[0]].strftime('%Y-%m-%d')
            # else:
            #     a['user21'] = '--'
            #     a['data21'] = '--'
            # ### 31
            # user=  data[(data['sfg']==sfg_list[i]) & (data['op_id']==31)]
            # if not user.empty:
            #     a['user31'] = user['user'][user.index[0]].last_name + user['user'][user.index[0]].first_name
            #     a['data31'] = user['date'][user.index[0]].strftime('%Y-%m-%d')
            # else:
            #     a['user31'] = '--'
            #     a['data31'] = '--'
            # #####
            # user=  data[(data['sfg']==sfg_list[i]) & (data['op_id']==41)]
            # if not user.empty:
            #     a['user41'] = user['user'][user.index[0]].last_name + user['user'][user.index[0]].first_name
            #     a['data41'] = user['date'][user.index[0]].strftime('%Y-%m-%d')
            # else:
            #     a['user41'] = '--'
            #     a['data41'] = '--'

            # user=  data[(data['sfg']==sfg_list[i]) & (data['op_id']==51)]
            # if not user.empty:
            #     a['user51'] = user['user'][user.index[0]].last_name + user['user'][user.index[0]].first_name
            #     a['data51'] = user['date'][user.index[0]].strftime('%Y-%m-%d')
            # else:
            #     a['user51'] = '--'
            #     a['data51'] = '--'

            # user=  data[(data['sfg']==sfg_list[i]) & (data['op_id']==60)]
            # if not user.empty:
            #     a['user60'] = user['user'][user.index[0]].last_name + user['user'][user.index[0]].first_name
            #     a['data60'] = user['date'][user.index[0]].strftime('%Y-%m-%d')
            # else:
            #     a['user60'] = '--'
            #     a['data60'] = '--'
            schedule_list.append(a)

        return render(request, 'report/schedule.html', {
            
            'schedule_list':schedule_list,
            'op_list':all_op_id,
            
            
        })
    else:
        return HttpResponse('It looks like no group assigned for you or there are no users under your groups. Pleas contact admin')
