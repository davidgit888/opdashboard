from django.shortcuts import render
from django.http import HttpResponse
from .models import Prob, Op, SfmProd, TypeStandard, Report
from datetime import date
from django.contrib.auth.decorators import login_required
import json

@login_required(login_url='/accounts/login/')  
def get_current_date_data(request, result):
    # username = request.user.last_name + request.user.first_name
    # result = Report.objects.filter(user=username, date=date.today())
    list_logs=[]
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
        list_logs.append(a)
    return list_logs

@login_required(login_url='/accounts/login/')  
def get_kpi(request):
    username = request.user.last_name + request.user.first_name
    result_today = Report.objects.filter(user=username, date=date.today())
    kpi_today = get_current_date_data(request,result_today)
    real_time_today =0
    stand_tiem_today =0
    for i in kpi_today:
        real_time_today += i['real']
        stand_tiem_today += i['standard']
    return real_time_today, stand_tiem_today

# when load the page
@login_required(login_url='/accounts/login/')  
def index(request):
    probs = Prob.objects.all()
    ops = Op.objects.all()
    groups = request.user.groups.all().values()
    group=None
    #get current username and report history for today
    username = request.user.last_name + request.user.first_name
    result_today = Report.objects.filter(user=username, date=date.today())
    history_logs = get_current_date_data(request,result_today)

    real_time_today, stand_time_today = get_kpi(request)
    today_kpi = round(stand_time_today/real_time_today,2)
    for i in groups:
        if '检验组' in i['name']:
            group = 1
    
    return render(request, 'report/report_get.html', {
        'op_list':ops,
        'prob_list':probs,
        'groups':group,
        'logs':history_logs,
        'today_kpi':today_kpi,
        

    })

# when click submit to save to database
@login_required(login_url='/accounts/login/')  
def get_data(request):
    probs = Prob.objects.all()
    ops = Op.objects.all()
    groups = request.user.groups.all().values()
    username = request.user.last_name + request.user.first_name
    result_today = Report.objects.filter(user=username, date=date.today())
    history_logs = get_current_date_data(request,result_today)
    group=None
    for i in groups:
        if '检验组' in i['name']:
            group = 1
    sfg = request.POST['sfg_id']
    type = request.POST['type']
    op_id = request.POST['op_id']
    prob_info = request.POST['prob_info']
    user = request.POST['user_name']
    standard_time = request.POST['standard_time']
    real_time = request.POST['real_time']
    qty = request.POST['qty']
    f_sfg = SfmProd.objects.get(sfg_id=sfg)
    f_op = Op.objects.get(op_id=op_id)
    query = Report(sfg_id=f_sfg,type_name=type,op_id=f_op,prob=prob_info,qty=qty,user=user,standard_tiem=standard_time,real_time=real_time)
    if prob_info== ' ':
        prob_info=None
    try:
        query.save()
        save_message="保存成功"
    except Exception as ex:    
        template = " An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)

        save_message = '保存失败'+ message
    #制造工时
    real_time = request.POST['real_time']

    return render(request,'report/report_get.html',{
        'save_message':save_message,
        'logs':history_logs,
        

    })
    # except:
    #     return render(request,'report/report_get.html',{
    #         'op':ops,
    #         'prob':probs,
    #     })
        
    #     return HttpResponse(isinstance(real_time,float))


# when click submit to save supportive data
@login_required(login_url='/accounts/login/')  
def supportive_time(request):
    support_time = request.POST['supportive_time']
    borrow_time = request.POST['borrow_time']

    return render(request, 'report/report_get.html',{
        'support':support_time,
        'borrow':borrow_time,
    })

@login_required(login_url='/accounts/login/')  
def get_sfgid(request):
    a = int(request.GET.get('a'))
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
    
    if prob == ' ':
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
            result = {'result':standart_time}
        except:
            result = {'result':'无标准工时'}
        return HttpResponse(json.dumps(result), content_type='application/json')
