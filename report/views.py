from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Prob, Op, SfmProd, TypeStandard, Report,SupportiveTime
from datetime import date
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
import json

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
def get_supportive_history(request,result):
    supportive_logs=[]
    list_total = [ [] for i in range(20)]
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
        list_total[0] += a['rest']
        list_total[1] += a['clean']
        list_total[2] += a['inside_group']
        list_total[3] += a['outside_group']
        list_total[4] += a['complete_machine']
        list_total[5] += a['granite']
        list_total[6] += a['prob']
        list_total[7] += a['shortage']
        list_total[8] += a['plan_change']
        list_total[9] += a['human_quality_issue_rework']
        list_total[10] += a['item_quality_issue']
        list_total[11] += a['human_quality_issue_repair']
        list_total[12] += a['equipment_mantainence']
        list_total[13] += a['inventory_check']
        list_total[14] += a['quality_check']
        list_total[15] += a['document']
        list_total[16] += a['group_management']
        list_total[17] += a['conference']
        list_total[18] += a['record']
        
        supportive_logs.append(a)
    list_total[19] = '汇总'
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
    a['date'] = list_total[19]
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
        if '检验组' in i['name']:
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
    return render(request, 'report/report_get.html', {
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
        

    })

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
        save_message="保存成功"
        return render(request, 'report/report_get.html', {
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

    })
    except Exception as ex:    
        template = "保存失败"
        message = template + json.dumps(ex.args)
        probs, ops, group, history_logs, today_kpi, month_kpi, year_kpi, supportive_logs,supportive_total = load_all_data(request)
        return render(request, 'report/report_get.html', {
            'op_list':ops,
            'prob_list':probs,
            'groups':group,
            'logs':history_logs,
            'today_kpi':today_kpi,
            'month_kpi':month_kpi,
            'year_kpi':year_kpi,
            'save_message':message,
            'supportive_logs':supportive_logs,
            'supportive_total':supportive_total,
         })
    
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
    
    try:    

        f_user = User.objects.get(id=request.user.id)
        query = SupportiveTime(user=f_user,rest=rest,clean_time=clean,inside_group=inside_group,outside_group=outside_group,
        complete_machine=complete_machine,granite=granite,prob=prob,shortage=shortage,plan_change=plan_change,
        human_quality_issue_rework=human_quality_issue_rework,item_quality_issue=item_quality_issue,human_quality_issue_repair=human_quality_issue_repair,
        equipment_mantainence=equipment_mantainence,inventory_check=inventory_check,quality_check=quality_check,
        document=document,conference=conference,group_management=group_management,record=record,date=date_time)

        query.save()
        probs, ops, group, history_logs, today_kpi, month_kpi, year_kpi, supportive_logs,supportive_total = load_all_data(request)
        save_message="保存成功"
        
        return render(request, 'report/report_get.html', {
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
            
                
            

        })
    except Exception as ex:    
        template = "保存失败"
        message = template + json.dumps(ex.args)
        probs, ops, group, history_logs, today_kpi, month_kpi, year_kpi, supportive_logs,supportive_total = load_all_data(request)
        return render(request, 'report/report_get.html', {
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
         })
    


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

def report_analysis(request):
    return HttpResponse('Comming Soon')
