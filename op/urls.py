from django.urls import path
from django.conf.urls import url
from . import views
from . import sites
from . import productionUpdate
from django.utils.encoding import iri_to_uri


app_name = 'op'
urlpatterns = [
    path('',views.loginIndex,name='index'),
    path('loginAuth/', views.dashboard, name='auth'),
    path('installed_cmm/', views.InstalledCmm),
    path('login/', views.loginIndex),
    path('plan/', views.plan),
    path('dashboard/', views.dashboard),
    path('dashboard/supplier/', views.supplier),
    path('dashboard/overdue/', views.overdue),
    path('dashboard/shortage/', views.shortage),
    path('dashboard/reason/', views.reason),
    path('dashboard/plans/supplier/', views.supplier),
    path('dashboard/plans/overdue/', views.overdue),
    path('dashboard/plans/shortage/', views.shortage),
    path('dashboard/plans/reason/', views.reason),
    path('dashboard/Installed_CMM/', sites.Installed_CMM),
    path('dashboard/Delivered_CMM/', sites.Delivered_CMM),
    path('dashboard/New_order/', sites.New_order),
    path('dashboard/Installed_each_year/', sites.Installed_each_year),
    path('dashboard/Installed_each_year_bar/', sites.Installed_each_year_bar),
    path('dashboard/Waiting_Order_and_Inventory/', sites.Waiting_Order_and_Inventory),
    path('dashboard/produced/Installed_CMM/', sites.Installed_CMM),
    path('dashboard/produced/Delivered_CMM/', sites.Delivered_CMM),
    path('dashboard/produced/New_order/', sites.New_order),
    path('dashboard/produced/Installed_each_year/', sites.Installed_each_year),
    path('dashboard/produced/Installed_each_year_bar/', sites.Installed_each_year_bar),
    path('dashboard/produced/Waiting_Order_and_Inventory/', sites.Waiting_Order_and_Inventory),
    path('dashboard/produced/', sites.produced),
    url(r'dashboard/生产制造/', sites.produced),
    path('dashboard/配置缺件/', sites.plan),
    path('dashboard/plans/', sites.plan),
    path('dashboard/logout.html', views.logoutUser),
    path('dashboard/logout/', views.logoutUser),
    path('dashboard/管理页面.html/', views.adminUtl),
    path('dashboard/update/', views.updateData),
    path('dashboard/Admin/', views.adminUtl),
    path('updateProduction/', views.updateProductionData),


]