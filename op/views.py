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



# check login details and redirect

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
    userId = User.objects.get(username=request.user.username).groups.values()
    user_group_list=[]
    for i in range(len(userId)):
        user_group_list.append(userId[i]['id'])

    user_all_permissions = []

    # groups = Group.objects.get(id=userId).permissions.values()
    for i in range(len(user_group_list)):
        group = Group.objects.get(id=user_group_list[i]).permissions.values()
        for j in range(len(group)):
            user_all_permissions.append(group[j]['name'])

    navList = get_user_permissions(user_all_permissions)
    return navList

@login_required(login_url='/accounts/login/')
def dashboard(request):
    
    navList = userAllPermisions(request)
    # navList = ['生产制造','配置缺件']
    if request.user.is_staff:
        admin = 'Admin'
        update = 'update'
    else:
        admin = ''
        update = ''
    if request.user.username == 'admin':
        log = 'log'
    else:
        log = ''
    return render(request,'op/index-dashboard.html',{
            'List':json.dumps(navList),
            'admin':admin,
            'update':update,
            'log':log,
        })

        # Redirect to a success page.
        


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
    return render(request, 'op/配置缺件.html')

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
    logs = LogEntry.objects.all()[:100]
    list_logs = get_all_logs(logs)
    return render(request, 'op/log.html', {
        'messages':list_logs,
    })

@login_required(login_url='/accounts/login/')
def updateShortageData(request):
    results = update_shortage()
    user_permission = userAllPermisions(request)
    update_shortage_list = get_update_list(user_permission)
   
    update_shortage_list['shortageMessage'] = json.dumps(results)
    return render(request,'op/updateList.html',update_shortage_list)