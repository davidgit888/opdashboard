
def get_user_permissions(data):
    navList = []
    for i in range(len(data)):
        if "生产" in data[i]:
            navList.append('生产制造')
        if 'overdue' in data[i]:
            navList.append('配置缺件')

    navList = list(set(navList))
    navList.sort()
    return navList

def get_update_list(data):
    
    update_list = {}
    for i in range(len(data)):
        if '生产制造' in data[i]:
            update_list['produced']='生产制造'
        if '配置缺件' in data[i]:
            update_list['shortage']='配置缺件'

    return update_list