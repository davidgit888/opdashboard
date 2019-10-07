from django.urls import path, include
from django.conf.urls import url
from . import views

app_name = 'valuehour'

urlpatterns = [
    # path('',views.index),
    # path('test/',views.test),
    path('saveManHours/', views.saveManHours),
    path('getStandardHours/', views.getStandardHours),
    path('getProductType/', views.getProductType),
    path('getWorkerOpProb/', views.getWorkerOpProb),
    path('saveAssistance/', views.saveAssistance),
    path('updateWorkerValue/', views.updateWorkerValue),
    path('saveOvertime/',views.saveOvertime),
    path('getManAssiOverValue/',views.getManAssiOverValue),
    path('getManHoursSurplus/', views.getManHoursSurplus),
    path('getBorrowType/', views.getBorrowType),
    path('jsonTest/', views.jsonTest),
    path('add_info/', views.addInfo, name='add_info'),
    path('getRecoverate/', views.getRecoverate, name='getRecoverate'),
    path('getWorkerValue/', views.getWorkerValue, name='getWorkerValue'),
    path('uploadFiles/', views.uploadFiles, name='uploadFiles'),
    path('downloadFile/', views.downloadFile, name='downloadFile'),
    path('getSimulation/', views.getSimulation, name='getSimulation'),
    ## template
    path('', views.index, name = 'valuehour'),
    path('baogong/', views.employee, name = 'baogong'),
    path('shenhe/', views.foreman, name = 'shenhe'),
    path('machine_submit/', views.machineSubmit, name = 'machine_submit'),
    path('assis_submit/', views.assisSubmit, name = 'assis_submit'),
    path('extra_submit/', views.extraSubmit, name = 'extra_submit'),
    path('get_machine/', views.getMachine, name = 'get_machine'),
    path('form_ms/', views.getMs, name='form_ms'),
    #### test templates ######
    path('testBase/', views.testBase, name='testBase'),
    path('testIndex/', views.testIndex, name='testIndex'),
    path('testPage/', views.testPage),
    path('header/', views.testHeader),
    path('getReportWuhao/', views.getReportWuhao),
    path('getScheduleGantt/', views.getScheduleGantt),
    path('getScheduleMaterial/', views.getScheduleMaterial),
]