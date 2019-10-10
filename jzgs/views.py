from django.shortcuts import render, redirect
from django.http import HttpResponse,FileResponse,Http404
import json
from .models import ManHours, Assistance, AssisType, UserInfomation,BorrowType,GroupPermissions,Permissions
from django.contrib.auth.models import User
from report.models import Op, Report,TypeStandard,Prob,SfmProd,GroupOp,OverTime,WorkGroups,SupportiveTime,TraceLog, GroupPerform,CoefficientSupport
from django.contrib.auth.decorators import login_required
import datetime
from django.core import serializers
import pandas as pd
import math
from django import forms
import uuid
import os
from django.core.serializers.json import DjangoJSONEncoder
from django.utils.encoding import escape_uri_path
# Create your views here.

@login_required(login_url='/accounts/login/') 
def index(request):
	return render(request, 'valuehour/production/index.html')

# @login_required(login_url='/accounts/login/') 
# def test(request):
# 	sfg = request.POST.get('sfg')
# 	op = request.POST.get('op')
	
# 	data = {
# 		"data":sfg,
# 		"user":op,
# 	}
# 	return HttpResponse(json.dumps(data))

@login_required(login_url='/accounts/login/') 
def saveManHours(request):
	"""制造工时"""
	data = request.POST.get('data')
	data = json.loads(data)
	contract = data['contract']
	sfg = data['sfg']
	product_type = data['product_type']
	op = float(data['op'])
	prob = data['prob']
	qty = float(data['qty'])
	standard = float(data['standard'])
	real_time = float(data['real_time'])
	cost_rate = float(data['cost_rate'])
	quote = float(data['quote'])
	date_time = data['date']
	original_group = data['original_group']
	work_group = data['work_group']
	# user_id = data['user_id']
	user_id = request.user.id
	exit_qty = manHourSurplus(sfg,op)
	old_standard = data['old_standard']
	if exit_qty == 0 and op !=11:
		return HttpResponse(json.dumps('保存失败, 数量已经是1'))
	# try:
	# f_user = User.objects.get(id=request.user.id)
	elif exit_qty < qty and op != 11:
		return HttpResponse(json.dumps('保存失败, 数量已经超过'+ str(exit_qty)))

	else:
		f_user = User.objects.get(id=user_id)
		f_op = Op.objects.get(op_id=op)
		queryOld = Report(sfg_id=sfg,type_name=product_type,op_id=f_op,prob=prob,qty=qty,user=f_user,standard_tiem=old_standard,
					real_time=real_time,date=date_time,groups=work_group)
		queryOld.save()
		flex = '{"old_report_id":'+str(queryOld.id)+',"old_standard":'+old_standard+"}"
		query = ManHours(contract=contract, sfg=sfg, product_type=product_type, op=f_op, prob=prob, qty=qty, username=f_user, 
			standard=standard, real_time=real_time, quote=quote, cost_rate=cost_rate, date=date_time, original_group=original_group,
			work_group=work_group, is_active=True, flexible=flex)
		query.save()
		
		message = json.dumps("success")
		return HttpResponse(message)
	# except Exception as e:

	# 	return HttpResponse(json.dumps(e.args))

@login_required(login_url='/accounts/login/')
def getManHoursSurplus(request):
	sfg = request.GET.get('sfg')
	op = request.GET.get('op')
	qty_surplus = manHourSurplus(sfg, op)
	return HttpResponse(qty_surplus,2)

def manHourSurplus(sfg, op):
	"""Get how many qty left 
	"""
	f_op = Op.objects.get(op_id=op)
	# data = ManHours.objects.values('qty').filter(is_active=1, date=date, username=user, sfg=sfg)
	data = ManHours.objects.values('qty').filter(is_active=True, sfg=sfg,op=f_op)
	all_qty = 0
	if(data):
		for i in range(len(data)):
			all_qty += data[i]['qty']
	else:
		all_qty = 0
	return round(1-all_qty,2)


def userInfo(user):
	""" get cost_rate and quote, original group, work group by user
		user is a list
	"""
	if 1 in user:
		user.remove(1)
	data = UserInfomation.objects.all().filter(user_id__in=user, is_active=True)
	items = []
	for i in range(len(data)):
		result = {}
		result['user_id'] = data[i].user_id.id
		result['full_name'] = data[i].user_id.get_full_name()
		result['cost_rate'] = data[i].cost_rate
		result['quote'] = data[i].quote
		result['original_group'] = data[i].original_group
		result['work_group'] = data[i].work_group.group_name
		result['flexible'] = data[i].flexible
		items.append(result)


	return items

@login_required(login_url='/accounts/login/')
def getStandardHours(request):
	"""Get standard value hours
	"""
	product_type = request.GET.get('product_type')
	op = request.GET.get('op')
	prob = request.GET.get('prob')
	if prob=='':
		prob = None
	else:
		prob = Prob.objects.get(prob_info=prob)
	try:
		standard_time = TypeStandard.objects.get(op_id=op,type_name=product_type,prob_info=prob).standard_time
	except:
		standard_time = ' '
	return HttpResponse(json.dumps(standard_time))

@login_required(login_url='/accounts/login/')
def getProductType(request):
	"""
	get Product type by sfg id
	"""
	sfg = request.GET.get('sfg')
	try:
		data = SfmProd.objects.filter(sfg_id=sfg).values('type_name')
		product_type = []
		for i in data:
			product_type.append(i['type_name'])		
	except:
		product_type = None
	return HttpResponse(json.dumps(product_type))

@login_required(login_url='/accounts/login/')
def getBorrowType(request):
	assis = AssisType.objects.filter(is_active=True).values('a_type','a_category','a_subject')
	borrow = BorrowType.objects.values('b_category','b_subject')
	data = {}
	data['category'] = list(assis)
	data['borrow'] = list(borrow)
	return HttpResponse(json.dumps(data))

@login_required(login_url='/accounts/login/')
def getWorkerOpProb(request):
	user_id = request.user.id
	prob_list = porbList(user_id) 
	work_group = userWorkGroup(user_id)
	op_list = opsList(user_id)
	result = {}
	is_foreman = isForeman(user_id)
	is_worker = isWorker(user_id)
	is_manager = isManager(user_id)
	is_electric = isElectric(user_id)
	user_role = UserInfomation.objects.get(user_id=user_id, is_active=True).duty
	if is_foreman and not is_electric:
		user_ids = userIdByWorkGroup(work_group)
		users = userInfo(user_ids) 
	elif is_worker:
		users = userInfo([user_id])
	elif is_manager:
		user_ids = User.objects.all().values('id')
		user_ids = changeDictToList(user_ids,'id')
		users = userInfo(user_ids)
	elif is_electric and is_foreman:
		user_ids = userIdByWorkGroup(work_group)
		user_ids += userIdByWorkGroup('数据-检验')
		users = userInfo(user_ids) 

	else:
		users = []
	result['prob']=prob_list
	result['op_list']=op_list
	result['user'] = users
	result['role'] = user_role
	return HttpResponse(json.dumps(result))

##### used functions ########
def allWorkGroups():
	""" Get all Work Groups
	"""
	work_groups = WorkGroups.objects.values('group_name')
	data = []
	for i in work_groups:
		data.append(i['group_name'])
	return data

def workgroupUserForeman(request):
	"""
	   get all users ids in list
	"""
	work_group = UserInfomation.objects.get(user_id=request.user.id, is_active=True).work_group
	users = UserInfomation.objects.filter(work_group=work_group, is_active=True).values('user_id')
	user_ids = []
	for i in range(len(users)):
		user_ids.append(users[i]['user_id'])

	return user_ids



def userWorkGroup(user):
	work_group = UserInfomation.objects.get(user_id=user, is_active=True).work_group.group_name
	return work_group


def opsList(user_id):
	work_group = userWorkGroup(user_id)
	op = GroupOp.objects.filter(group_name=work_group)
	op_list = []
	for i in range(len(op)):
		a = {'op_id':op[i].op_id.op_id,'op_name':op[i].op_id.op_name}
		op_list.append(a)
	return op_list

def isElectric(user):
	work_group = userWorkGroup(user)
	is_electric = False
	# if any('班组长' and '电气' in word for word in orginal_group):
	# if any('电气' or '检验' in word for word in work_group):
	if '电气' in work_group  or '检验' in work_group:
		is_electric = True
	return is_electric

def porbList(user):
	is_electric = isElectric(user)
	if is_electric:
		prob = list(Prob.objects.all().values('prob_info'))
	else:
		prob = None
	return prob




def userIdByWorkGroup(work_group):
	f_work_group = WorkGroups.objects.get(group_name=work_group)
	ids = UserInfomation.objects.filter(work_group=f_work_group, is_active=True).values('user_id')
	ids = changeDictToList(list(ids),'user_id')
	return ids

@login_required(login_url='/accounts/login/')
def saveAssistance(request):
	data = request.POST.get('data')
	data = json.loads(data)
	contract = data['contract']
	# a_type = data['a_type']
	a_subject = data['a_subject']
	real_time = data['real_time']
	quote = data['quote']
	cost_rate = data['cost_rate']
	standard = data['standard']
	expense = data['expense']
	original_group = data['original_group']
	work_group = data['work_group']
	date = data['date']
	comments = data['comments']
	b_category = data['b_category']
	b_subject = data['b_subject']
	try:
		expense_hour = data['expense_hour']
	except:
		expense_hour=0
	# return HttpResponse(json.dumps(data))
	quality_no = data['quality_no'] #质量单号
	f_user = User.objects.get(id=request.user.id)
	category = AssisType.objects.get(a_subject=a_subject, is_active=True)
	a_type=category.a_type
	a_category = category.a_category
	old_id = saveOldSupportiveTime(f_user, a_type, a_subject, real_time, comments, date, work_group)
	if old_id == 0:
		return HttpResponse("Failed")
	flex = {"old_supportive_id":old_id,"quality_no":quality_no,"expense_hour":expense_hour}
	query = Assistance(contract=contract, a_type=a_type, a_category=a_category, a_subject=a_subject, real_time=real_time,quote=quote,
		cost_rate=cost_rate, standard=standard, expense=expense, original_group=original_group, work_group=work_group,
		username=f_user, date=date, is_active=True, comments = comments, flexible=json.dumps(flex), b_category=b_category,
		b_subject=b_subject)
	query.save()
	return HttpResponse(json.dumps('success'))

def saveOldSupportiveTime(user, a_type, a_subject, real_time, comments, date, work_group):
	data = {}
	data['休息'] = 'rest'
	data['卫生'] = 'clean_time'
	data['组内'] = 'inside_group'
	data['整机'] = 'complete_machine'
	data['花岗石'] = 'granite'
	data['物流搬运'] = 'prob'
	data['补缺件'] = 'shortage'
	data['计划调整'] = 'plan_change'
	data['人为质量问题返工'] = 'human_quality_issue_repair'
	data['零件质量问题'] = 'item_quality_issue'
	data['设备维护'] = 'equipment_mantainence'
	data['库存核查'] = 'inventory_check'
	data['质量审核'] = 'quality_check'
	data['档案整理'] = 'document'
	data['会议'] = 'conference'
	data['班组管理'] = 'group_management'
	data['记录'] = 'record'
	data['组外'] = 'outside_group'
	data['线性/垂直度修正'] = 'vertical'
	data['人为质量问题返修'] = 'human_quality_issue_rework'
	if a_type in ['其他辅助工时','计提工时','质量工时','辅助制造工时']:
		try:
			reference = AssisType.objects.get(a_subject=a_subject, is_active=True).b_old_category
			field = data[reference]
			query = SupportiveTime(**{field:real_time}, user=user, date=date, groups=work_group,comments=comments)
			query.save()
			return query.id
		except Exception as e:
			full_name = User.objects.get(id=user)
			saveTraceLog(user, full_name.get_full_name(), "Save Old 辅助工时", "Faild" + json.dumps(e.args),
				a_type+a_subject+str(real_time)+work_group)
			return 0
	elif a_type == '外部工时':
		query = SupportiveTime(user=user, borrow_time=real_time, borrow_name=a_subject, date=date, groups=work_group,comments=comments)
		query.save()
		return query.id
	else:
		return 0
	return query.id

def saveTraceLog(user, username, action, detail, comments):
	if isinstance(user, int):
		f_user = User.objects.get(id=user)
	else:
		f_user = User.objects.get(username=user)
	try:
		query = TraceLog(user=f_user, username=username, action_log = action, detail_message=detail, comments=comments)
		query.save()
	except Exception as e:
		query = TraceLog(user=f_user, username=username, action_log = "Trace Log Failed", detail_message="Reason is: "+json.dumps(e.args), 
			comments=detail)

@login_required(login_url='/accounts/login/')
def updateWorkerValue(request):
	"""update and delete ManHours and Assistance
	"""
	items = request.POST.get('data')
	# return HttpResponse(items) 
	items = json.loads(items)
	# return HttpResponse(json.dumps(items))
	all_data = items['data']
	message = ""
	for data in all_data:
		try:
			data.pop('csrfmiddlewaretoken')
		except:
			pass
		info_id = data['id']
		info_type = data['type']
		action = data['action']
		user = User.objects.get(id=request.user.id).get_full_name()
		if info_type == 'machine':
			if action == 'update':
				confirmed = data['confirmed']
				try:
					ManHours.objects.filter(id=info_id, is_active=True).update(confirmed=confirmed,last_fix_user=user,last_fix_status=data,
						last_fix_date=datetime.datetime.now())
					# return HttpResponse(json.dumps('success'))
					message = "success"
				except Exception as e:
					return HttpResponse("保存失败"+json.dumps(e.args))
			if action == 'delete':
				ManHours.objects.filter(id=info_id, is_active=True).update(is_active=False,last_fix_user=user,last_fix_status=data,
					last_fix_date=datetime.datetime.now())
				try:
					old_report = json.loads(ManHours.objects.get(id=info_id).flexible)
					old_report_id = old_report['old_report_id']
					Report.objects.filter(id=old_report_id).delete()
					saveTraceLog(request.user.id, user, "ManHours Delete","Success",data)
					# return HttpResponse(json.dumps('success'))
					message = "success"
				except Exception as e:
					saveTraceLog(request.user.id, user, "ManHours Delete","Faild"+json.dumps(e.args),data)
					return HttpResponse("删除失败"+json.dumps(e.args))

		if info_type == 'assistance':
			if action == 'update':
				confirmed = data['confirmed']
				b_category = data['b_category']
				b_subject = data['b_subject']
				expense = data['expense']
				comments = data['comments']
				expense_hour = data['expense_hour']
				flex = json.loads(Assistance.objects.get(id=info_id).flexible)
				flex['expense_hour'] = expense_hour
				Assistance.objects.filter(id=info_id, is_active=True).update(b_category = b_category, b_subject = b_subject,
					expense = expense, comments = comments, last_fix_date = datetime.datetime.now(),
					last_fix_user = user, last_fix_status = data, confirmed=confirmed, flexible=json.dumps(flex))
				# return HttpResponse(json.dumps('success'))
				message = "success"
			if action == 'delete':
				Assistance.objects.filter(id=info_id, is_active=True).update(is_active=False,last_fix_date = datetime.datetime.now(),
					last_fix_user = user, last_fix_status = data)
				try:
					old_assist = json.loads(Assistance.objects.get(id=info_id).flexible)
					old_assist_id = old_assist['old_supportive_id']
					SupportiveTime.objects.filter(id=old_assist_id).delete()
					saveTraceLog(request.user.id, user, "Old SupportiveTime Delete","Success",data)
					# return HttpResponse(json.dumps('success'))
					message = "success"
				except Exception as e:
					saveTraceLog(request.user.id, user, "Assistance Delete","Faild"+json.dumps(e.args),data)
					return HttpResponse(json.dumps(e.args))
		if info_type == 'overtime':
			if action == 'delete':
				try:
					OverTime.objects.filter(id=info_id).delete()
					saveTraceLog(request.user.id, user, "Overtime Delete","Successful",data)
					return HttpResponse(json.dumps('success'))
					message = "success"
				except:
					saveTraceLog(request.user.id, user, "Overtime Delete","Faild because: "+json.dumps(e.args),data)

	return HttpResponse(json.dumps(message))

@login_required(login_url='/accounts/login/')
def saveOvertime(request):
	"""save over time
	"""
	data = request.POST.get('data')
	data = json.loads(data)
	f_user = User.objects.get(id=request.user.id)
	over_time = data['hour']
	over_time_type = data['category']
	is_paid = data['fee']
	date = data['date']
	work_group = userWorkGroup(request.user.id)
	query = OverTime(user=f_user, over_time=over_time, over_time_type=over_time_type, is_paid=is_paid, groups=work_group,date=date)
	query.save()
	return HttpResponse(json.dumps('success'))
	

def orginalGroups(user):
	""" get all original groups
	"""
	all_groups = []
	user = User.objects.get(id=user)
	groups = user.groups
	for i in groups.select_related():
		all_groups.append(i.name)
	return all_groups

def isManager(user):
	""" is report manager
	"""
	all_groups = orginalGroups(user)
	if '报工平台-主管' in all_groups:
		return True
	else:
		return False


def isForeman(user):
	all_groups = orginalGroups(user)
	if "报工平台-班组长" in all_groups and '报工平台-主管' not in all_groups:
		return True

	else:
		return False

def isWorker(user):
	all_groups = orginalGroups(user)
	if "报工平台-员工" in all_groups and "报工平台-班组长" not in all_groups and '报工平台-主管' not in all_groups:
		return True
	else:
		return False



def userIdByWorkGroupDate(user_id, date):
	work_group = userWorkGroup(user_id)
	if isinstance(date, list):
		man_id = ManHours.objects.filter(work_group=work_group, date__range=(date[0],date[1]), is_active=True).values('username')
		ass_id = Assistance.objects.filter(work_group=work_group, date__range=(date[0],date[1]), is_active=True).values('username')
	else:	
		man_id = ManHours.objects.filter(work_group=work_group, date=date, is_active=True).values('username')
		ass_id = Assistance.objects.filter(work_group=work_group, date=date, is_active=True).values('username')
	result = list(man_id)
	result += list(ass_id)
	result = changeDictToList(result,'username')
	result = list(set(result))
	return result

@login_required(login_url='/accounts/login/')
def getManAssiOverValue(request):
	""" get all manhour, assitance and overtime
	"""
	user_id = request.user.id
	is_foreman = isForeman(user_id)
	is_manager = isManager(user_id)
	is_worker = isWorker(user_id)
	is_electric = isElectric(user_id)
	date = request.GET.get('date')
	end_date = request.GET.get('end_date')
	if end_date:
		date = [date, end_date]
	m_names = [field.name for field in ManHours._meta.fields]
	m_fields = [i for i in m_names if i not in ('last_fix_user', 'last_fix_status', 'is_active', 'flexible','create_date','last_fix_date')]
	data = {}
	if is_foreman:
		all_user_ids = userIdByWorkGroupDate(user_id, date)
		work_group = userWorkGroup(user_id)	
	elif is_manager:
		user_ids = User.objects.filter(is_active=True).values('id')
		all_user_ids = changeDictToList(list(user_ids), 'id')
		work_group = 0
	elif is_worker:
		all_user_ids = [request.user.id]
		work_group = 0
	else:
		return HttpResponse("No access")
	
	if is_electric and not is_manager and is_foreman:
		# add 数据-检验 users
		elec_user_ids = userIdByWorkGroupDate(85, date)
		for i in elec_user_ids:
			data_type = {}
			a = {}
			result = workerValue(i, date, '数据-检验')
			a[i] = result
			data_type['machine'] = a[i]
			b = {}
			ass_result = assistValue(i, date, '数据-检验')
			b[i] = ass_result
			data_type['assistance'] = b[i]
			c = {}
			over_result = overtimeValue(i, date, '数据-检验')
			c[i] = over_result
			data_type['overtime'] = c[i]
			data[i] = data_type			
	for i in all_user_ids:
		data_type = {}
		a = {}
		result = workerValue(i, date, work_group)
		if result is not None:
			data_type['machine']=result
		# data[i] = data_type
		b = {}
		ass_result = assistValue(i, date, work_group)
		if ass_result is not None:
			data_type['assistance'] = ass_result
		c = {}
		over_result = overtimeValue(i, date, work_group)
		if over_result is not None:
			data_type['overtime'] =over_result
		if result is not None or ass_result is not None or over_result is not None:
			data[i] = data_type
	return HttpResponse(json.dumps(data, cls=DjangoJSONEncoder))


def workerValue(user, date, work_group):
	""" get single or worker ManHours
	"""
	if work_group == 0:
		if isinstance(date, list):
			result = ManHours.objects.filter(username = user, is_active=True, date__range=(date[0],date[1])).values('id','contract',
				'sfg','product_type','op_id__op_id','prob','qty','username','standard','real_time','confirmed',
			'quote','cost_rate','original_group','work_group','flexible','date','username__first_name','username__last_name')
		else:
			result = ManHours.objects.filter(username = user, is_active=True, date=date).values('id','contract','sfg','product_type',
				'op_id__op_id','prob','qty','username','standard','real_time','confirmed',
			'quote','cost_rate','original_group','work_group','flexible','date','username__first_name','username__last_name')
	else:
		if isinstance(date, list):
			result = ManHours.objects.filter(username = user, is_active=True, date__range=(date[0],date[1]), work_group=work_group).values('id','contract',
				'sfg','product_type','op_id__op_id','prob','qty','username','standard','real_time','confirmed',
			'quote','cost_rate','original_group','work_group','flexible','date','username__first_name','username__last_name')
		else:
			result = ManHours.objects.filter(username = user, is_active=True, date=date, work_group=work_group).values('id','contract','sfg','product_type',
				'op_id__op_id','prob','qty','username','standard','real_time','confirmed',
			'quote','cost_rate','original_group','work_group','flexible','date','username__first_name','username__last_name')
	if len(result) == 0:
		return None
	data = []
	for i in list(result):
		a = {}
		a['id'] = i['id']
		a['contract'] = i['contract']
		a['sfg'] = i['sfg']
		a['product_type'] = i['product_type']
		a['op_id__op_id'] = i['op_id__op_id']
		a['prob'] = i['prob']
		a['username'] = i['username__last_name']+i['username__first_name']
		a['qty'] = i['qty']
		a['standard'] = i['standard']
		a['real_time'] = i['real_time']
		a['confirmed'] = i['confirmed']
		a['quote'] = i['quote']
		a['cost_rate'] = i['cost_rate']
		a['original_group'] = i['original_group']
		a['work_group'] = i['work_group']
		a['flexible'] = i['flexible']
		a['date'] = i['date']
		data.append(a)
	return data

def assistValue(user, date, work_group):
	"""get assitance values for worker Assistance
	"""
	if work_group == 0:
		if isinstance(date, list):
			result = Assistance.objects.filter(username = user, is_active=True, date__range=(date[0],date[1])).values('id','contract','a_type',
				'a_category','a_subject','real_time','quote','cost_rate','username','standard','confirmed','attach','b_category',
				'b_subject','expense','original_group','work_group','comments','flexible','date','username__first_name','username__last_name')
		else:

			result = Assistance.objects.filter(username = user, is_active=True, date=date).values('id','contract','a_type',
			'a_category','a_subject','real_time','quote','cost_rate','username','standard','confirmed','attach','b_category',
			'b_subject','expense','original_group','work_group','comments','flexible','date','username__first_name','username__last_name')
	else:
		if isinstance(date, list):
			result = Assistance.objects.filter(username = user, is_active=True, date__range=(date[0],date[1]), work_group=work_group).values('id','contract','a_type',
				'a_category','a_subject','real_time','quote','cost_rate','username','standard','confirmed','attach','b_category',
				'b_subject','expense','original_group','work_group','comments','flexible','date','username__first_name','username__last_name')
		else:

			result = Assistance.objects.filter(username = user, is_active=True, date=date, work_group=work_group).values('id','contract','a_type',
			'a_category','a_subject','real_time','quote','cost_rate','username','standard','confirmed','attach','b_category',
			'b_subject','expense','original_group','work_group','comments','flexible','date','username__first_name','username__last_name')

	if len(result) == 0:
		return None
	data = []
	for i in list(result):
		a = {}
		a['id'] = i['id']
		a['contract'] = i['contract']
		a['a_category'] = i['a_category']
		a['a_subject'] = i['a_subject']
		a['attach'] = i['attach']
		a['b_category'] = i['b_category']
		a['username'] = i['username__last_name']+i['username__first_name']
		a['a_type'] = i['a_type']
		a['standard'] = i['standard']
		a['real_time'] = i['real_time']
		a['confirmed'] = i['confirmed']
		a['quote'] = i['quote']
		a['cost_rate'] = i['cost_rate']
		a['original_group'] = i['original_group']
		a['work_group'] = i['work_group']
		a['flexible'] = i['flexible']
		a['date'] = i['date']
		a['b_subject'] = i['b_subject']
		a['expense'] = i['expense']
		a['comments'] = i['comments']
		data.append(a)		
	return data

def overtimeValue(user, date, work_group):
	if work_group == 0:
		if isinstance(date, list):
			result = OverTime.objects.filter(user=user,date__range=(date[0],date[1])).values('id','user','over_time',
				'over_time_type','is_paid','groups','date','user__first_name','user__last_name')
		else:
			result = OverTime.objects.filter(user=user,date=date).values('id','user','over_time','over_time_type',
				'date','is_paid','groups','user__first_name','user__last_name')
	else:
		if isinstance(date, list):
			result = OverTime.objects.filter(user=user,date__range=(date[0],date[1]), groups=work_group).values('id','user',
				'date','over_time','over_time_type','is_paid','groups','user__first_name','user__last_name')
		else:
			result = OverTime.objects.filter(user=user,date=date, groups=work_group).values('id','user','over_time',
				'over_time_type','is_paid','groups','date','user__first_name','user__last_name')
	if len(result)==0:
		return None
	data = []
	for i in list(result):
		a={}
		a['id'] = i['id']
		a['user'] = i['user__last_name'] + i['user__first_name']
		a['date'] = i['date']
		a['over_time'] = i['over_time']
		a['is_paid'] = i['is_paid']
		a['over_time_type'] = i['over_time_type']
		a['groups'] = i['groups']
		data.append(a)

	return list(data)

def changeDictToList(data, key):
	result = [x[key] for x in data]
	return result


def sumManValue(from_date, to_date, work_group, value_type):
	""" Get A recoverate = (A+C) / (A+B+C)
	A;
	"""
	if isinstance(work_group, int):
		# get only on user's value
		hours = ManHours.objects.filter(date__range=(from_date,to_date),username=work_group, is_active=True).values(value_type)

	elif work_group != "ALL":
		hours = ManHours.objects.filter(date__range=(from_date,to_date),work_group=work_group, is_active=True).values(value_type)
	else:
		hours = ManHours.objects.filter(date__range=(from_date,to_date), is_active=True).values(value_type)

	data = pd.DataFrame(list(hours))
	if len(data) == 0:
		total = 0
	else:
		total = data.sum()[0]
	return round(total,2)

def sumAssisValue(from_date, to_date, work_group, value_type):
	""" get B for recover rate
	"""
	if isinstance(work_group, int):
		hours = Assistance.objects.filter(date__range=(from_date,to_date),username=work_group, a_type__in=value_type, is_active=True).values('confirmed')
	elif work_group != "ALL":
		hours = Assistance.objects.filter(date__range=(from_date,to_date),work_group=work_group, a_type__in=value_type, is_active=True).values('confirmed')
	else:
		hours = Assistance.objects.filter(date__range=(from_date,to_date), a_type__in=value_type, is_active=True).values('confirmed')
	data = pd.DataFrame(list(hours))
	if len(data) == 0:
		total = 0
	else:	
		total = data.sum()[0]
	return round(total,2)

def sumBorrowValue(from_date, to_date, work_group):
	""" get C for recover rate
	"""
	if isinstance(work_group, int):
		hours = Assistance.objects.filter(date__range=(from_date,to_date),username=work_group, a_type__in=['外部工时','质量工时','计提工时'], is_active=True).values('confirmed')
	elif work_group != "ALL":
		hours = Assistance.objects.filter(date__range=(from_date,to_date),work_group=work_group, a_type__in=['外部工时','质量工时','计提工时'], is_active=True).values('confirmed')
	else:
		hours = Assistance.objects.filter(date__range=(from_date,to_date), a_type__in=['外部工时','质量工时','计提工时'], is_active=True).values('confirmed')
	data = pd.DataFrame(list(hours))
	if len(data) == 0:
		total = 0
	else:
		total = data.sum()[0]
	return round(total,2)


def sumExpenseValue(from_date, to_date, work_group):
	""" Get expense horus, sigma
	"""
	if isinstance(work_group, int):
		hours = Assistance.objects.filter(date__range=(from_date,to_date),username=work_group, is_active=True).values('flexible')
	elif work_group != "ALL":
		hours = Assistance.objects.filter(date__range=(from_date,to_date),work_group=work_group, is_active=True).values('flexible')
	else:
		hours = Assistance.objects.filter(date__range=(from_date,to_date), is_active=True).values('flexible')
	data = list(hours)
	# expense = [json.loads(i['flexible'])['expense_hour'] for i in data]
	total = 0
	for i in data:
		try:
			a = json.loads(i['flexible'])['expense_hour']
			total += a
		except:
			pass
	# total = sum(expense)
	return round(total, 2)

def calRecoverate(from_date, to_date, work_group):
	"""
	calculate recoverate for foreman 
	"""
	b = sumAssisValue(from_date, to_date, work_group,['辅助制造工时','其他辅助工时'])
	a = sumManValue(from_date, to_date, work_group,'confirmed')
	c = sumBorrowValue(from_date, to_date, work_group)
	# e = sumExpenseValue(from_date, to_date, work_group)
	if a+b+c == 0:
		recover_rate = 0
	else:
		recover_rate = (a+c)/(a+b+c)
	# return "a: is "+str(a) + "b: "+str(b)+"c: "+str(c)+"e: "+str(e)
	return round(recover_rate,2)

def getSimulation(request):
	from_date, to_date = fromToDate(0,0)
	user_id = request.user.id
	work_group = userWorkGroup(user_id)
	data = {}
	man = sumManValue(from_date, to_date, work_group,'confirmed')
	assis = sumAssisValue(from_date, to_date, work_group,['辅助制造工时','其他辅助工时'])
	borrow = sumBorrowValue(from_date, to_date, work_group)
	# expense = sumExpenseValue(from_date, to_date, work_group)
	data['分子']= man + borrow
	data['分母']=man + borrow + assis
	return HttpResponse(json.dumps(data))

def calWorkerValue(from_date, to_date, user_id):
	"""
	calculate value for single user
	"""
	is_foreman = isForeman(user_id)
	is_worker = isWorker(user_id)
	is_manager = isManager(user_id)
	if is_worker:
		work_group = user_id
	elif is_foreman:
		work_group = userWorkGroup(user_id)
	else:
		work_group = 'ALL'
	a = sumManValue(from_date, to_date, work_group, 'confirmed')
	b = sumAssisValue(from_date, to_date, work_group,['辅助制造工时','其他辅助工时'])
	c = sumBorrowValue(from_date, to_date, work_group)
	return round(a+b+c, 2)

def fromToDate(quarter, year):
	today = datetime.date.today()
	quarter = int(quarter)
	year = int(year)
	if year == 0:
		year = today.year
	if quarter == 1:
		from_date = today.replace(year=year,month=1,day=1)
		to_date = today.replace(year=year, month=3, day=31)
	elif quarter == 2:
		from_date = today.replace(year=year,month=4,day=1)
		to_date = today.replace(year=year, month=6, day=30)
	elif quarter == 3:
		from_date = today.replace(year=year,month=7,day=1)
		to_date = today.replace(year=year, month=9, day=30)
	elif quarter == 4:
		from_date = today.replace(year=year,month=10,day=1)
		to_date = today.replace(year=year, month=12, day=31)
	elif quarter == 0:
		quarter = math.ceil(today.month/3)
		from_date, to_date = fromToDate(quarter, today.year)
	else:
		from_date = today.replace(year=year,month=1,day=1)
		to_date = today.replace(year=year,month=12,day=31)
	return from_date, to_date

@login_required(login_url='/accounts/login/')
def getRecoverate(request):
	user_id = request.user.id
	quarter = request.GET.get('quarter')
	year = request.GET.get('year')
	if quarter is None:
		quarter = 0
	if year is None:
		year = 0
	recoverate = {}
	is_foreman = isForeman(user_id)
	is_manager = isManager(user_id)
	all_work_groups = allWorkGroups()
	# return HttpResponse(str(quarter+year))
	from_date, to_date = fromToDate(quarter, year)
	if is_manager:
		for i in all_work_groups:
			total = calRecoverate(from_date, to_date, i)
			recoverate[i]=total
		total = calRecoverate(from_date, to_date, 'ALL')
		recoverate['ALL'] = total
	elif is_foreman:
		work_group = userWorkGroup(user_id)
		recoverate[work_group] = calRecoverate(from_date, to_date, work_group)
	return HttpResponse(json.dumps(recoverate))

@login_required(login_url='/accounts/login/')
def getWorkerValue(request):
	user_id = request.user.id
	quarter = request.GET.get('quarter')
	year = request.GET.get('year')
	if quarter is None:
		quarter = 0
	if year is None:
		year = 0
	from_date, to_date = fromToDate(quarter, year)
	year_from_date, year_to_date = fromToDate(9,0)
	if quarter is not None and year is not None:
		whole_year = calWorkerValue(year_from_date, year_to_date, user_id)
	else:
		whole_year = None
	this_quarter = calWorkerValue(from_date, to_date, user_id)
	a = {}
	a['whole_year'] = whole_year
	a['this_quarter'] = this_quarter
	return HttpResponse(json.dumps(a))


@login_required(login_url='/accounts/login/')
def uploadFiles(request):
	if request.method == 'POST':
		# try:
		assis_id = request.POST.get('id')
		f = request.FILES['file']
		baseName = os.path.abspath(os.path.dirname(__file__))
		path = baseName.replace('jzgs','files')
		ext = f.name.split('.')[1]
		if ext not in ['jpg','png','zip','7z','xlsx','csv','pdf','doc','ppt','rar','msg','txt','docx','xls','tif','gif','jpeg','xlsm']:
			return HttpResponse('Failed, file type is not allowed to upload')
		fileName = str(uuid.uuid4())+datetime.datetime.now().strftime("%y-%m-%d-%H-%M-%S") + "__" + f.name
		with open(os.path.join(path,fileName), 'wb+') as destination:
			for chunk in f.chunks():
				destination.write(chunk)
		Assistance.objects.filter(id=assis_id, is_active=True).update(attach=fileName)
		return HttpResponse("success" + str(assis_id))
	# except Exception as e:
		# 	return HttpResponse(json.dumps(e.args))

@login_required(login_url='/accounts/login/')
def downloadFile(request):
	assis_id = request.GET.get('id')
	fileName = Assistance.objects.get(id=assis_id, is_active=True).attach
	baseName = os.path.abspath(os.path.dirname(__file__))
	path = baseName.replace('jzgs','files')
	name = fileName.split('__')[1]
	response = FileResponse(open(os.path.join(path,fileName), 'rb'))
	response['content_type'] = "application/octet-stream"
	response['Content-Disposition'] = 'attachment; filename= "%s"' % escape_uri_path(name)
	return response

def userMenuList(user_id):
	a = User.objects.get(id=user_id).groups

	group_list = []
	for i in a.select_related():
		group_list.append(i.id)
	group_permissions = GroupPermissions.objects.filter(group__in=group_list)
	permission_list = []
	for i in range(len(group_permissions)):
		a = list(group_permissions[i].permissions.values('title','subtitle','subtitle2','url'))
		permission_list += a 

	user_permissions = list(UserInfomation.objects.get(user_id=user_id).permissions.values('title','subtitle','subtitle2','url').order_by('title'))
	permission_list += user_permissions
	permission_list = removeDuplicateJson(permission_list)
	return permission_list


def removeDuplicateJson(data):
	result = []
	for x in data:
		if x not in result:
			result.append(x)
	return result

##### templates #####
@login_required(login_url='/accounts/login/')
def employee(request):
	return render(request, 'valuehour/production/tables.html') # 员工报工页面

@login_required(login_url='/accounts/login/')
def foreman(request):
	return render(request, 'valuehour/production/tables_dynamic.html') # 班组长审核页面

@login_required(login_url='/accounts/login/')
def machineSubmit(request):
	return render(request, 'valuehour/production/form_machine.html') # 员工报制造工时

@login_required(login_url='/accounts/login/')
def assisSubmit(request):
	return render(request, 'valuehour/production/form_assis.html') # 员工报辅助工时

@login_required(login_url='/accounts/login/')
def extraSubmit(request):
	return render(request, 'valuehour/production/form_borrow.html') # 员工加班时

@login_required(login_url='/accounts/login/')
def getMachine(request):
	try:
		if request.method == 'POST':
			res = json.dumps(request.POST)
			if res:
				return HttpResponse('success')
			else:
				return HttpResponse('No Data')
		else:
			return HttpResponse('需要使用POST提交数据')
	except Exception as e:
		return HttpResponse(e)

@login_required(login_url='/accounts/login/')
def test1(request):
	return render(request, 'valuehour/production/base.html')

@login_required(login_url='/accounts/login/')
def addInfo(request):
	return render(request, 'valuehour/production/form_accomplish.html')

##### test #######
@login_required(login_url='/accounts/login/')
def jsonTest(request):
	data = request.POST.get('data')
	data = json.loads(data)
	items = data['data']
	item_list = []
	for i in items:
		item_list.append(i['id'])
	return HttpResponse(json.dumps(item_list))

@login_required(login_url='/accounts/login/')
def getMs(request):
	return render(request, 'valuehour/production/form_ms.html')


##### test templates #######
@login_required(login_url='/accounts/login/')
def testIndex(request):
	aaa=[]
	data = {}
	dataAppend = [
		{'sublevel':'数据报表','url':"/jzgs/"},
		{'sublevel':'小部件','url':"/jzgs/testIndex/"},
	]
	data2Append = [
		{'sublevel':'报工页面','url':"/jzgs/baogong//"},
	]
	data3Append = [
		{'sublevel':'班组长确认','url':"/jzgs/shenhe/"},
	]
	data1 = {}
	data['title'] = '<li id="nav_data"><a><i class="fa fa-bar-chart-o"></i> 数据报表 <span class="fa fa-chevron-down"></span></a>'
	data['content'] = dataAppend
	aaa.append(data)
	data1['title'] = '<li id="nav_baogong" style="display: none;"><a><i class="fa fa-edit"></i> 现场报工 <span class="fa fa-chevron-down"></span></a>'
	data1['content'] = data2Append
	aaa.append(data1)
	data2 = {}
	data2['title'] = '<li id="nav_shenhe" style="display: none;"><a><i class="fa fa-check-circle-o"></i> 工时确认 <span class="fa fa-chevron-down"></span></a>'
	data2['content'] = data3Append
	aaa.append(data2)
	return render(request, 'jzgs/index.html', {
		"data":aaa,
		})
	# return render(request, 'jzgs/index.html')

def testPage(request):
	return render(request, 'jzgs/page.html')

def updateCostReateInManAssis():
	""" update the standard time if cost_rate has changed
	"""
	data = UserInfomation.objects.values('user_id','cost_rate')
	df = pd.DataFrame(list(data),columns=['user_id','cost_rate'])
	mans = list(ManHours.objects.filter(is_active=1).values('id','username__id','sfg','product_type','op__op_id','prob','qty'))
	assis = list(Assistance.objects.filter(is_active=1).values('id','username__id','real_time'))
	for i in range(len(mans)):
		product_type = mans[i]['product_type']
		op = mans[i]['op__op_id']
		if mans[i]['prob'] == '':
			prob = None
		else:
			prob = Prob.objects.get(prob_info=mans[i]['prob'])
		standard = float(TypeStandard.objects.get(op_id=op,type_name=product_type,prob_info=prob).standard_time)
		cost_rate = float(df[df['user_id']==mans[i]['username__id']]['cost_rate'])
		qty = float(mans[i]['qty'])
		if cost_rate !=0:
			value = round(290*standard*qty/cost_rate, 2)
		else:
			value = 0
		if value:
			ManHours.objects.filter(id=mans[i]['id']).update(standard=value)
		else:
			saveTraceLog(mans[i]['username__id'],mans[i]['username__id'] , 'update manhour value', 'failed', 'id is: '+str(mans[i]['id']))
	for i in range(len(assis)):
		cost_rate = float(df[df['user_id']==assis[i]['username__id']]['cost_rate'])
		qty = float(assis[i]['real_time'])
		if cost_rate !=0:
			value = round(100*qty/cost_rate,2)
		else:
			value = 0
		if value:
			Assistance.objects.filter(id=assis[i]['id']).update(standard=value)
		else:
			saveTraceLog(assis[i]['username__id'],assis[i]['username__id'] , 'update assis value', 'failed', 'id is: '+str(assis[i]['id']))

def updateCostRateInUserInfo():
	mans = list(ManHours.objects.filter(is_active=1).values('id','username'))
	data = UserInfomation.objects.values('user_id','cost_rate')
	df = pd.DataFrame(list(data),columns=['user_id','cost_rate'])
	for i in range(len(mans)):
		cost_rate = float(df[df['user_id']==mans[i]['username']]['cost_rate'])
		ManHours.objects.filter(id=mans[i]['id']).update(cost_rate=cost_rate)
	assis = list(Assistance.objects.filter(is_active=1).values('id','username'))
	for i in range(len(assis)):
		cost_rate = float(df[df['user_id']==assis[i]['username']]['cost_rate'])
		Assistance.objects.filter(id=assis[i]['id']).update(cost_rate=cost_rate)

def updateReportStandardTime(from_date, to_date):
	data = list(Report.objects.filter(date__range=[from_date, to_date]).values('id','user','standard_tiem','type_name',
		'op_id__op_id','prob','qty'))
	for i in range(len(data)):
		product_type = data[i]['type_name']
		op = data[i]['op_id__op_id']
		if data[i]['prob'] == '':
			prob = None
		else:
			prob = Prob.objects.get(prob_info=data[i]['prob'])
		standard = float(TypeStandard.objects.get(op_id=op,type_name=product_type,prob_info=prob).standard_time)
		standard = standard * data[i]['qty']
		Report.objects.filter(id=data[i]['id']).update(standard_tiem=standard)
	return "yes"

### test base.html with menu list access ####
###### Main Page #######
@login_required(login_url='/accounts/login/')
def testBase(request):
	# all_perms = list(Permissions.objects.values('title').distinct())
	user_perms = userMenuList(request.user.id)
	df = pd.DataFrame(user_perms,columns=['title','subtitle2'])
	titles = df['title'].unique()
	data = []
	icons = {
		"信息采集模块":"fa fa-home",
		"信息应用模块":"fa fa-desktop",
		"生产仪表板":"fa fa-bar-chart-o",
		"基础信息模块":"fa fa-laptop",
		"追溯记录":"fa fa-bug",

	}
	for i in range(len(titles)):
		a = {}
		a['title'] = titles[i]
		try: 
			a['icon'] = icons[titles[i]]
		except:
			a['icon'] = "fa fa-bug"
		b = []
		for j in range(len(user_perms)):
			c = {}
			if user_perms[j]['title'] == titles[i]:
				print(user_perms[j]['subtitle'])
				print(user_perms[j]['url'])
				c['subtitle'] = user_perms[j]['subtitle']
				c['url'] = user_perms[j]['url']
				# print(c)
				b.append(c)
				print("######")
				# print(b)
		a['content'] = b
		data.append(a)
	f = open("../system.txt")
	sys_env = f.read()

	return render(request, 'jzgs/base.html', {
		"data":data,
		'sys_env':sys_env,
		})

def testHeader(request):
	return render(request, 'jzgs/header.html')


@login_required(login_url='/accounts/login/')
def getReportWuhao(request):
	return render(request, 'jzgs/report_wuhao.html')

@login_required(login_url='/accounts/login/')
def getScheduleGantt(request):
	return redirect('/report/getScheduleTable/')


@login_required(login_url='/accounts/login/')
def getScheduleMaterial(request):
	return redirect("/report/getScheduleMaterial/")


# @login_required(login_url='/accounts/login/')
# def getReportWuhao(request):
# 	return render(request, 'jzgs/report_wuhao.html')


# @login_required(login_url='/accounts/login/')
# def getReportWuhao(request):
# 	return render(request, 'jzgs/report_wuhao.html')

# @login_required(login_url='/accounts/login/')
# def getReportWuhao(request):
# 	return render(request, 'jzgs/report_wuhao.html')

# @login_required(login_url='/accounts/login/')
# def getReportWuhao(request):
# 	return render(request, 'jzgs/report_wuhao.html')