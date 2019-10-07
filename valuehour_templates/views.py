from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json


# Create your views here.
def index(request):
	return render(request, 'valuehour/production/index.html')

def employee(request):
	return render(request, 'valuehour/production/tables.html')

def foreman(request):
	return render(request, 'valuehour/production/tables_dynamic.html')

def machineSubmit(request):
	return render(request, 'valuehour/production/form_machine.html')

def assisSubmit(request):
	return render(request, 'valuehour/production/form_assis.html')

def extraSubmit(request):
	return render(request, 'valuehour/production/form_borrow.html')

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