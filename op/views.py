from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
import json
from .permissions import get_user_permissions, get_update_list, get_all_logs
from .productionUpdate import updateProduction
from django.contrib.admin.models import LogEntry
from .shortageUpdate import update_shortage
from report.models import TraceLog
from django.template import loader
from pyecharts import Line3D
import math
from time import sleep
# check login details and redirect
REMOTE_HOST = "https://pyecharts.github.io/assets/js"

def loginIndex(request):
   

    if 'username' in request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        
        # navList = ['生产制造','配置缺件']
        if user is not None:
            
            login(request, user)
            # return render(request,'dash/index-dashboard.html',{
            #     'List':json.dumps(navList)
            # })
            # Redirect to a success page.
            # admin='ADMIN'
            return HttpResponseRedirect('/op/dashboard/')
        else:
            return render(request, 'op/login.html', {
                'error_message':'用户名或密码错误'
            })
    else:
        return render(request, 'op/login.html')
#check navList to identify the permission of user
def userAllPermisions(request):
    # userId = User.objects.get(username=request.user.username).groups.values()
    # user_group_list=[]
    # for i in range(len(userId)):
    #     user_group_list.append(userId[i]['id'])

    # user_all_permissions = []

    # # groups = Group.objects.get(id=userId).permissions.values()
    # for i in range(len(user_group_list)):
    #     group = Group.objects.get(id=user_group_list[i]).permissions.values()
    #     for j in range(len(group)):
    #         user_all_permissions.append(group[j]['name'])
    user_all_permissions = []
    user = User.objects.get(id=request.user.id)
    groups = user.groups
    for i in groups.select_related():
        user_all_permissions.append(i.name)

    navList = get_user_permissions(user_all_permissions)
    return navList

@login_required(login_url='/accounts/login/')
def dashboard(request):
    
    # navList = userAllPermisions(request)
    # # navList = ['生产制造','配置缺件']
    # if request.user.is_staff:
    #     admin = 'Admin'
    #     update = ''
    # else:
    #     admin = ''
    #     update = ''
    # if request.user.username == 'admin':
    #     log = 'log'
    #     update = 'update'
    # else:
    #     log = ''
    # f = open("../system.txt")
    # sys_env = f.read()
    # return render(request,'op/index-dashboard.html',{
    #         'List':json.dumps(navList),
    #         'admin':admin,
    #         'update':update,
    #         'log':log,
    #         'sys_env':sys_env,
    #     })

    return HttpResponseRedirect("/jzgs/testBase/")

        # Redirect to a success page.

@login_required(login_url='/accounts/login/')       
def report(request):
    return HttpResponseRedirect('/jzgs/')

def report_analysis(request):
    return HttpResponseRedirect('/report/report_analysis/')

@login_required(login_url='/accounts/login/')
def InstalledCmm(request):
    return render(request,'op/Installed CMM.html')


@login_required(login_url='/accounts/login/')
def updateData(request):
    user_permission = userAllPermisions(request)
    update_list = get_update_list(user_permission)
    return render(request, 'op/updateList.html', update_list)
   
@login_required(login_url='/accounts/login/')
def dash(request):
    return render(request, 'op/dash.html')

@login_required(login_url='/accounts/login/')
def plan(request):
    template = loader.get_template('echarts/echarts.html')
    l3d = line3d()
    context = dict(
        myechart=l3d.render_embed(),
        host=REMOTE_HOST,
        script_list=l3d.get_js_dependencies()
    )
    return HttpResponse(template.render(context, request))




def line3d():
    _data = []
    for t in range(0, 25000):
        _t = t / 1000
        x = (1 + 0.25 * math.cos(75 * _t)) * math.cos(_t)
        y = (1 + 0.25 * math.cos(75 * _t)) * math.sin(_t)
        z = _t + 2.0 * math.sin(75 * _t)
        _data.append([x, y, z])
    range_color = [
        '#313695', '#4575b4', '#74add1', '#abd9e9', '#e0f3f8', '#ffffbf',
        '#fee090', '#fdae61', '#f46d43', '#d73027', '#a50026']
    line3d = Line3D("3D line plot demo", width=1200, height=600)
    line3d.add("", _data, is_visualmap=True,
               visual_range_color=range_color, visual_range=[0, 30],
               is_grid3D_rotate=True, grid3D_rotate_speed=180)
    return line3d

# @login_required(login_url='')
# def dashboard(request):
#     navList = ['生产制造','配置缺件']
#     return render(request, 'dash/index-dashboard.html',{
#         'List':json.dumps(navList)
#         })

@login_required(login_url='/accounts/login/')
def supplier(request):
    return render(request, 'op/supplier.html')

@login_required(login_url='/accounts/login/')
def overdue(request):
    return render(request, 'op/overdue.html')

@login_required(login_url='/accounts/login/')
def shortage(request):
    return render(request, 'op/shortage.html')

@login_required(login_url='/accounts/login/')
def reason(request):
    return render(request, 'op/reason.html')

def logoutUser(request):
    logout(request)
    return render(request, 'op/login.html', {
        'error_message':'您已成功注销'
    })

@login_required(login_url='/accounts/login/')   
def updateProductionData(request):
    results = updateProduction()
    user_permission = userAllPermisions(request)
    update_list = get_update_list(user_permission)

    update_list['producedMessage']=json.dumps(results)
    return render(request,'op/updateList.html',update_list)

@login_required(login_url='/accounts/login/')
def adminUtl(request):
    return HttpResponseRedirect('/admin')

@login_required(login_url='/accounts/login/')
def log(request):
    logs = LogEntry.objects.all()[:1000]
    log_list = []
    for i in range(len(logs)):
        a = {}
        a['time'] = logs[i].action_time.strftime("%Y-%m-%d %H:%M:%S")
        if logs[i].get_change_message():
            a['action'] = logs[i].get_change_message()
        else:
            a['action'] = logs[i].get_action_flag_display()
        a['url'] = logs[i].get_admin_url()
        try:
            a['chgd_user'] = logs[i].get_edited_object().get_full_name()
        except:
            a['chgd_user'] =logs[i].object_repr
        a['user'] = logs[i].user.get_full_name()
        a['details'] = logs[i].change_message
        log_list.append(a)
    # list_logs = get_all_logs(logs)
    trace_log_l = []
    trace_log = TraceLog.objects.all().values().order_by('-date')[:1000]
    for i in range(len(trace_log)):
        a = {}
        a['username']=trace_log[i]['username']
        a['action_log']=trace_log[i]['action_log']
        a['detail_message']=trace_log[i]['detail_message']
        a['comments'] = trace_log[i]['comments']
        a['date']=trace_log[i]['date'].strftime("%Y-%m-%d %H:%M:%S.%f")
        trace_log_l.append(a)
    return render(request, 'op/log.html', {
        'messages':log_list,
        'trace_log':trace_log_l,
    })

@login_required(login_url='/accounts/login/')
def updateShortageData(request):
    results = update_shortage()
    user_permission = userAllPermisions(request)
    update_shortage_list = get_update_list(user_permission)
   
    update_shortage_list['shortageMessage'] = json.dumps(results)
    return render(request,'op/updateList.html',update_shortage_list)

   