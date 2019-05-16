from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from .additional import Additional, TEMP_URL, REPORT, ADM_GROUPS
import json
import datetime
from .models import SheetConfig, Partlist, Specification, Record, SfmAjd
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from django.db.models import Count, Max, Sum
import os
import re
from django import template
from django.template.defaulttags import register
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import auth
from datetime import date
from dateutil.rrule import rrule, DAILY
from django.contrib.auth.models import User
from report.views import workGroupId,get_groups
from report.models import UserGroups, WorkGroups
# Create your views here.
# define the function to check if user in groups
def in_group(user):
	return user.groups.filter(name__in= ADM_GROUPS).exists()


@login_required
@user_passes_test(in_group)
def getQrCode(request, serial_no):
	qr = Additional()
	link = qr.make_code(serial_no)
	return render(request, 'smallparts/wi_form_qrcode.html', {'qrcode':link, 'serial_no':serial_no})

def GetTimeRange(delta = 30, str = None):
	time_start = datetime.date.today()
	time_end = time_start - datetime.timedelta(days = delta)
	date_list = []
	for dt in rrule(DAILY, dtstart = time_end, until = time_start):
		date_list.append(dt)
	if str:
		return [d.strftime("%Y_%m_%d") for d in date_list]
	else:
		return date_list

#checked - strict
def parse_str(group_id, version, string= False):
	config_str = SheetConfig.objects.get(group_id = group_id, version = version)
	config_string = config_str.config_string.replace('\n','').replace('\r','').replace(' ','')
	if not string:		
		config_list = config_string.split('$')[1:]
		result = {}
		item_list =[]
		for config_unit in config_list:
			config_unit_list = config_unit.split('|')
			result[config_unit_list[0].replace('.','_')] = config_unit_list[1:]
			item_list.append(config_unit_list[0])
		return result
	else:
		return config_string


@register.filter
def key(d, key_name):
	return d.get(key_name)[0]

@register.filter
def key1(d, key_name):
	return d.get(key_name)[1]

@register.filter
def res(d, key_name):
	return d.get('result'+key_name)

# @register.filter(name='has_group') 
# def has_group(user, group_name):
#     return user.groups.filter(name__in =group_name).exists()
@register.filter(name = 'has_group')
def has_group(user):
	return user.groups.filter(name__in = ADM_GROUPS).exists()

@register.filter
def com(d, key_name):
	return d.get('comment'+key_name)

@register.filter
def dat(d, key_name):
	return d.get('date'+key_name)

@register.filter
def tem_version(dic_str):
	dic = json.loads(dic_str)
	return dic['version']

@register.filter
def getorder(order_str):
	order_list = [r for r in order_str.split('/') if r != '']
	return order_list[-1]

def treat_dic(dic):
	l1 = list(dic.keys())
	l1 = [r.replace('.', '_') for r in l1]
	l2 = list(dic.values())
	return dict(zip(l1, l2))

def remove_file(path):
	if os.path.exists(path):
		try:
			os.remove(path)
		except Exception as e:
			return('error: %s' % e)

def back_dic(dic):
	l1 = list(dic.keys())
	l1 = [r.replace('_', '.') for r in l1]
	l2 = list(dic.values())
	return dict(zip(l1, l2))

#checked
def getversion(queryobject, group_id):
	obj = queryobject.objects.filter(group_id = group_id, is_active = 1).order_by('-version')[0]
	return obj

#checked!
@login_required
def index(request, part, ordernbr):
	try:
		group_id = Partlist.objects.get(name = part).group_id
		config_obj = getversion(SheetConfig, group_id) # get last version active WI
		specification = Specification.objects.get(part = part)
		machine = specification.machine
		title = config_obj.title
		version = config_obj.version
		config_string = config_obj.config_string.replace('\n','').replace('\r','').replace(' ','')
		config_list = config_string.split('$')[1:]
		result = {}
		item_list =[]
		item_unmust_list = []
		item_unmust_no_result = []
		for config_unit in config_list:
			config_unit_list = config_unit.split('|')
			result[config_unit_list[0]] = config_unit_list[1:]
			item_list.append(config_unit_list[0])
			if 'canbeopen' in config_unit_list:
				item_unmust_list.append('result'+config_unit_list[0])
				item_unmust_no_result.append(config_unit_list[0])
		request.session['posted'] = 'no'
		return render(request, 'smallparts/wi_form_blank.html', 
			{'title':title, 'part':part, 'date':datetime.datetime.now().strftime('%Y-%m-%d'), 
			'json_config':result, 'item_list':json.dumps(item_list), 'machine':machine, 'group_id':group_id, 
			'version':version, 'ordernbr':ordernbr, 'unmust':json.dumps(item_unmust_list), 'item_unmust_no_result':json.dumps(item_unmust_no_result)})
	except Exception as e:
		return HttpResponse('<script>alert("这种零部件还没有关联数据记录表，请联系班组长！%s"); window.location.href = "%s"</script>' % (e, reverse('smallparts:search')))

#checked
@login_required
def treatStr(request):
	try:
		if request.method =='POST' and request.session['posted'] == 'no':
			json_str = request.POST.get('json_str', None)
			if json_str:
				json_dic = json.loads(json_str)
				result_list = [re.match('comment(.+)', l).group(1).replace('.', '_') for l in json_dic.keys() if re.match('comment.+', l)]
				group_id = int(json_dic['group'])
				version = int(json_dic['version'])
				ordernbr = int(json_dic['ordernbr'])
				result = int(json_dic['result'])
				sntaken = json_dic.get('sntaken', None)
				sheet = SheetConfig.objects.get(group_id = group_id, version = version).id
				day_today = datetime.datetime.now().date()
				day_after = day_today + datetime.timedelta(days = 1)
				config_dic = parse_str(group_id, version)
				serial = Record.objects.filter(part = json_dic['part'], input_date__range = (day_today, day_after))
				if serial:
					serial_sequence = serial.values('part').annotate(count = Count('part')).values('count')[0]['count'] + 1
				else:
					serial_sequence = 1
				serial_no = json_dic['part']+'_'+str(ordernbr)+datetime.datetime.now().strftime('_%y%m%d_')+str(serial_sequence)
				if sntaken:
					serial_no+= '_'+sntaken
				rec = Record(serial_no = serial_no, record_string = json_str, machine_type = json_dic['machine'], 
					part = json_dic['part'], sheet_config_id_id = sheet, result = result, operator = json_dic['operator'], order_no = ordernbr)
				rec.save()
				ad = Additional()
				link = ad.make_code(serial_no)
				pdf = ad.export_pdf(request.get_host(), serial_no)
				request.session['posted'] = 'yes'
				return render(request, 'smallparts/wi_form_success.html', {'json_dic':treat_dic(json_dic), 
					'config_dic':config_dic, 'result_list': result_list, 'qrcode':link, 'serial_no':serial_no, 'pdf':pdf, 'version':version, 'ordernbr':ordernbr})
		else:
			return HttpResponse('禁止刷新重复提交，请前往搜索页</br><a href = "%s">点击转到搜索页</a>' % reverse('smallparts:search'))
	except Exception as e:
		return HttpResponse('发生错误：%s,联系管理员' % e)

#checked
def print_template(request, serial_no):
	try:
		json_str = Record.objects.get(serial_no = serial_no).record_string
		json_dic = json.loads(json_str)
		group_id = json_dic['group']
		version = json_dic['version']
		config_dic = parse_str(group_id, version)
		result_list = [re.match('comment(.+)', l).group(1).replace('.', '_') for l in json_dic.keys() if re.match('comment.+', l)]
		return render(request, 'smallparts/wi_form_print.html', {'config_dic':config_dic, 'json_dic':treat_dic(json_dic), 
			'result_list':result_list, 'serial_no':serial_no, 'version':version})
	except Exception as e:
		return HttpResponse('发生错误：%s,联系管理员' % e)
#checked
@login_required
def search(request):
	specification = Specification.objects.all().values_list('part', flat = True)
	parts = Partlist.objects.all().distinct().values_list('name', flat = True).order_by('name')
	parts = list(set(specification).intersection(set(parts))) 
	parts = sorted(parts)
	return render(request, 'smallparts/wi_form_search.html', {'parts':parts})


@login_required
def history(request, nbr = 2000, ongoing = None):
	groups = get_groups(request)
	# return HttpResponse(groups)
	group_list =[]
	for i in groups:
		if '数据' in i:
			group_list.append(i)

	user_list=[]
	for i in group_list:
		groups = workGroupId(i)
		user_list += groups


	if request.user.groups.filter(name__in= ADM_GROUPS).exists():
		operator_ids = user_list
		operators = User.objects.filter(id__in = operator_ids).values_list('username', flat = True)
		result = Record.objects.filter(operator__in = operators).order_by('-id')
	else:
		result = Record.objects.filter(operator = request.user.username).order_by('-id')
	ongoing = result.filter(result = 2).count()
	finish = result.filter(result = 1).count()
	deleted = result.filter(result = 0).count()
	return render(request, 'smallparts/wi_form_history.html', {'result':result, 'ongoing':ongoing, 'finish':finish, 'deleted':deleted})


@login_required
def change(request, id):
	record = Record.objects.get(pk = id)
	json_str = record.record_string
	serial_no = record.serial_no
	json_dic = json.loads(json_str)
	group_id = json_dic['group']
	version = json_dic['version']
	config_string = parse_str(group_id, version, True)
	config_dic = parse_str(group_id, version, False)
	config_string = config_string.replace('\n','').replace('\r','').replace(' ','')
	config_list = config_string.split('$')[1:]
	item_list =[]
	item_unmust_list = []
	for config_unit in config_list:
		config_unit_list = config_unit.split('|')
		item_list.append(config_unit_list[0].replace('.','_'))
		if 'canbeopen' in config_unit_list:
			item_unmust_list.append('result'+config_unit_list[0].replace('.','_'))
	result_list = [re.match('comment(.+)', l).group(1).replace('.', '_') for l in json_dic.keys() if re.match('comment.+', l)]
	return render(request, 'smallparts/wi_form_change.html', {'config_dic':config_dic, 'json_dic':treat_dic(json_dic), 
		'result_list':result_list, 'serial_no':serial_no, 'record_id':id, 'version':version, 'ordernbr':record.order_no,
		'item_list':json.dumps(item_list), 'unmust':json.dumps(item_unmust_list)})

#checked
@login_required
def update(request):
	try:
		target = request.POST.get('target', None)
		target_dic = json.loads(target)
		target_dic = back_dic(target_dic)
		record_id = target_dic['recordid']
		original_str = Record.objects.get(pk = record_id).record_string
		original_dic = json.loads(original_str)
		for target_key, target_value in target_dic.items():
			original_dic[target_key] = target_value
		del original_dic['recordid']
		original_str = json.dumps(original_dic, ensure_ascii = False)
		record = Record.objects.get(pk = record_id)
		record.record_string = original_str
		record.result = target_dic['result']
		record.save()

		serial_no = record.serial_no
		link = os.path.join(REPORT, '%s.pdf' % serial_no)
		remove_file(link)

		ad = Additional()
		ad.export_pdf(request.get_host(), serial_no)
		return HttpResponse('''<div style='font-size:48px; color:green; text-align:center; vertical-align: middle; padding-top:20%; '>
			更新成功！</div><script>setTimeout("var index = parent.layer.getFrameIndex(window.name); parent.layer.close(index);parent.location.reload();", 1500);</script>''')
	except Exception as e:
		return HttpResponse('''<div style='font-size:48px; color:red; text-align:center; vertical-align: middle; padding-top:20%; '>
			更新失败！</div><script>setTimeout("var index = parent.layer.getFrameIndex(window.name); parent.layer.close(index);parent.location.reload();", 1500);</script>''')
#checked
@login_required
@user_passes_test(in_group)
def markdel(request, record_id):
	try:
		record = Record.objects.get(pk = record_id)
		record_string = record.record_string
		record_dic = json.loads(record_string)
		record_dic['deleter'] = request.user.username
		record_string = json.dumps(record_dic, ensure_ascii = False)
		record.record_string = record_string
		record.result = 0
		record.save()
		return HttpResponse('success!')
	except exception as e:
		return HttpResponse(e)

def logout(request):
	auth.logout(request)
	return redirect('/admin/')

@login_required
@user_passes_test(in_group)
def pbm(request):
	return render(request, 'smallparts/pbm_submit.html')

@login_required
@user_passes_test(in_group)
def get_pbm(request):
	if request.method == 'POST':
		# return HttpResponse('pOST')
		
		shift = request.POST.get('shift', None)
		user_id = User.objects.get(username=shift)

		group_id = UserGroups.objects.get(user=user_id).work_group
		# return HttpResponse(group_id)
		shift = group_id
		# return HttpResponse(shift)
		# group_name = WorkGroups.objects.get(id=group_id).group_name
		# shift = group_name
		adj_date = request.POST.get('adj_date', None)
		adj_reason = request.POST.get('adj_reason', None)
		adj_nbr_shortage = request.POST.get('adj_nbr_shortage', None)
		adj_nbr_notfull = request.POST.get('adj_nbr_notfull', None)
		adj_nbr_granite = request.POST.get('adj_nbr_granite', None)
		adj_nbr_other = request.POST.get('adj_nbr_other', None)
		if not adj_nbr_shortage:
			if not adj_nbr_notfull:
				if not adj_nbr_granite:
					if not adj_nbr_other:
						return HttpResponse('没有填写任何数量')
		adj_list = ['adj_nbr_shortage', 'adj_nbr_notfull', 'adj_nbr_granite', 'adj_nbr_other']
		d = {'adj_nbr_shortage':'缺件', 'adj_nbr_notfull':'排产不饱满', 'adj_nbr_granite':'花岗石未进厂', 'adj_nbr_other':'其他'}
		pop = '%s成功提交成功：\n\n日期-%s\n\n' % (shift, adj_date)
		for adj in adj_list:
			if adj in request.POST and request.POST.get(adj) and request.POST.get(adj, None)!='0':
				sfm = SfmAjd()
				sfm.shift = shift
				sfm.adj_date = datetime.datetime.strptime(adj_date, '%Y/%m/%d')
				adj_reason = d[adj]
				adj_nbr = request.POST.get(adj, None)
				sfm.adj_nbr = adj_nbr
				sfm.adj_reason = adj_reason
				sfm.save()
				pop += '原因:%s ---- 数量:%s\n' % (adj_reason, str(adj_nbr))
		return HttpResponse(pop)
	else:
		return HttpResponse('please post something')

@register.filter
def GetSfm(d, k):
	calendar_30 = GetTimeRange(str = True)
	result_list = []
	for cal in calendar_30:
		key = k+'_'+cal
		result_list.append(d.get(key, 0))
	return result_list

@register.filter
def GetSfmDates(d):
	calendar_30 = GetTimeRange(str = True)
	result_list = []
	for cal in calendar_30:
		result_list.append(d.get(cal, 0))
	return result_list

@register.filter
def GetList(l, p):
	lis = l.split('_')
	return lis[p]


@login_required
@user_passes_test(in_group)
def sfmchart(request):
	# get all reasons and shifts
	adj_reasons = ['缺件','排产不饱满','花岗石未进厂', '其他']
	shifts = SfmAjd.objects.only('shift').distinct().values_list('shift', flat = True)
	shift_reason = [s +'_'+ r for s in shifts for r in adj_reasons]
	legends = shift_reason
	legends.append('总计')
	# get all dates
	calendar_30 = GetTimeRange(str = True)

	#get splited dic
	before = datetime.datetime.now() - datetime.timedelta(days = 40)
	sfm_reason = SfmAjd.objects.filter(adj_date__gt = before).values('shift', 'adj_date', 'adj_reason').annotate(qty = Sum('adj_nbr')).order_by('-adj_date')
	# result_reason = sfm_reason.values('shift','adj_date','adj_reason','qty').distinct().order_by('-adj_date')
	sfm_date = SfmAjd.objects.filter(adj_date__gt = before).values('adj_date').annotate(qty = Sum('adj_nbr')).order_by('-adj_date')

	dic_reason = {}
	for result in sfm_reason:
		key = result['shift']+'_'+result['adj_reason']+'_'+result['adj_date'].strftime('%Y_%m_%d')
		dic_reason[key] = result['qty']

	dic_dates = {}
	for sd in sfm_date:
		dic_dates[sd['adj_date'].strftime('%Y_%m_%d')] = sd['qty']

	return render(request, 'smallparts/pbm_statis.html', {'dic_reason':dic_reason, 'shift_reason':shift_reason, 
		'dates':calendar_30, 'dic_dates':dic_dates, 'legends':legends})

def clear_temp(request):
	dirToBeEmptied = TEMP_URL #需要清空的文件夹

	ds = list(os.walk(dirToBeEmptied)) #获得所有文件夹的信息列表
	delta = datetime.timedelta(days=2) #设定365天前的文件为过期
	now = datetime.datetime.now() #获取当前时间

	for d in ds: #遍历该列表
	    os.chdir(d[0]) #进入本级路径，防止找不到文件而报错
	    if d[2] != []: #如果该路径下有文件
	        for x in d[2]: #遍历这些文件
	            ctime = datetime.datetime.fromtimestamp(os.path.getctime(x)) #获取文件创建时间
	            if ctime < (now-delta): #若创建于delta天前
	                os.remove(x) #则删掉
	return HttpResponse('已经清除两天前的所有缓存')