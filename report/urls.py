
from django.urls import path, include
from django.conf.urls import url
from . import views


urlpatterns = [
    path('',views.index),
    #url(r'test/(?P<backend>\w+?)/',views.index),
    path('get_data/', views.get_data),
    path('supportive_time/', views.supportive_time),
    path('get_sfg/', views.get_sfgid),
    path('get_standard_time/',views.get_standard_time),
    path('report_analysis/',views.report_analysis),
    path('get_real_time_estimate/', views.get_real_time_estimate),
    path('get_prod_time_log/',views.get_produce_time_bytime),
    path('get_support_time_log/',views.get_support_time_log),
    path('per_get_prod_log/',views.per_get_prod_log),
    path('save_indiv_perform/', views.save_indiv_perform),
    path('get_sfg_comments/',views.get_sfg_comments),
    path('create_new_sfg_comments/',views.create_new_sfg_comments),
    path('update_sfg_comments/',views.update_sfg_comments),
    path('save_overtime_data/',views.save_overtime_data),
    path('group_statistic/',views.group_statistic),
    path('perform_pop/',views.perform_pop),
    path('kpi/',views.kpi_dash),
    path('create_docinfo/',views.create_docinfo),
    path('save_doc_info/',views.save_doc_info),
    path('search_docinfo/',views.search_docinfo),
    path('update_docinfo/',views.update_docinfo),
    path('dashboard/', views.dashBoard),
    path('opdetails/',views.opdetails),
    path('materialApprove/',views.materialApprove),
    path('materialGet/',views.materialGet),
    path('materialCheck/',views.materialCheck),
    path('getMaterialNo/',views.getMaterialNo),
    path('saveMaterialUse/',views.saveMaterialUse),
    path('saveMaterialApprove/',views.saveMaterialApprove),
    path('saveMaterialGet/',views.saveMaterialGet),
    path('saveMaterialSup/',views.saveMaterialSup),
    path('uploadMatrlAprv/',views.uploadMatrlAprv),
    path('getScheduleTable/', views.getScheduleTable),
    path('getSchedulePerform/', views.getSchedulePerform),
    path('getScheduleAnalysis/', views.getScheduleAnalysis),
    path('getScheduleMaterial/', views.getScheduleMaterial),
    
    #path('upload_excel/',)
]