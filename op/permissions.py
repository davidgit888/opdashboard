
from django.contrib.auth.models import User

def get_user_permissions(data):
    navList = []
    for i in range(len(data)):
        if "生产" in data[i]:
            navList.append('produced')
            navList.append('onsiteDash')
        # if '配置缺件' in data[i]:
        #     navList.append('plans')
        if '报工平台' in data[i]:
            navList.append('report')
        if '班组长' in data[i]:
            navList.append('reporAnalysis')
            navList.append('onsiteDash')
            navList.append('produced')

    navList = list(set(navList))
    navList.sort(reverse=True)
    return navList

def get_update_list(data):
    
    update_list = {}
    for i in range(len(data)):
        #生产制造
        if 'produced' in data[i]:
            update_list['produced']='生产制造'
        #配置缺件
        if 'plans' in data[i]:
            update_list['shortage']='配置缺件'

    return update_list

def get_all_logs(logs):
    list_logs=[]
    for i in range(len(logs)):
        a={}
        a['date']=logs[i].action_time.strftime("%Y-%m-%d %H:%M:%S")
        a['message'] = logs[i].change_message
        a['object'] = logs[i].object_repr
        a['id'] = User.objects.get(id=logs[i].user_id).username
        list_logs.append(a)
    return list_logs