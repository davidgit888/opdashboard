
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
    #path('upload_excel/',)
]