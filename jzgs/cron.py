import sys
import os
import django


sys.path.append("E:\OPDashboard\prod_environment\opdashboard")
os.environ.setdefault('DJANGO_SETTINGS_MODULE','dashboard.settings')
django.setup()

from report.models import Report

a = Report.objects.all()
print(len(a))