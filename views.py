from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json


# Create your views here.
def index(request):
	return render(request, 'valuehour/production/index.html') # 首页, 汇总页面

def employee(request):
	return render(request, 'valuehour/production/tables.html') # 员工报工页面

def foreman(request):
	return render(request, 'valuehour/production/tables_dynamic.html') # 班组长审核页面

def machineSubmit(request):
	return render(request, 'valuehour/production/form_machine.html') # 员工报制造工时

def assisSubmit(request):
	return render(request, 'valuehour/production/form_assis.html') # 员工报辅助工时

def extraSubmit(request):
	return render(request, 'valuehour/production/form_borrow.html') # 员工加班时

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

def test1(request):
	return render(request, 'valuehour/production/base/html')