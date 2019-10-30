from .models import ManHours
from report.models import Report
from .models import Assistance
from report.models import SupportiveTime


def getManHours(from_date, to_date, work_group):
	if work_group != 0:
		data = ManHours.objects.filter(date__range=[from_date, to_date], work_group=work_group, 
			is_active=True).exclude(confirmed=0).values('qty')
	else:
		data = ManHours.objects.filter(date__range=[from_date, to_date], 
			is_active=True).exclude(confirmed=0).values('qty')

	return data

def getReportHours(from_date, to_date, work_group):
	if work_group != 0:
		data = Report.objects.filter(date__range=[from_date, to_date], groups=work_group).values('qty')
	else:
		data = Report.objects.filter(date__range=[from_date, to_date]).values('qty')

	return data

def getAssistanceHours(from_date, to_date, work_group):
	if work_group != 0:
		data = Assistance.objects.filter(date__range=[from_date, to_date], work_group=work_group, 
			is_active=True).exclude(confirmed=0).values('real_time')
	else:
		data = ManHours.objects.filter(date__range=[from_date, to_date], 
			is_active=True).exclude(confirmed=0).values('real_time')

	return data

def getSupportiveHours(from_date, to_date, work_group):
	if work_group != 0:
		data = ManHours.objects.filter(date__range=[from_date, to_date], work_group=work_group, 
			is_active=True).exclude(confirmed=0).values()
	else:
		data = ManHours.objects.filter(date__range=[from_date, to_date], 
			is_active=True).exclude(confirmed=0).values()

	return data	
