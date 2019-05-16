"""parts URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from smallparts import views as spView
from django.urls import path

app_name = 'smallparts'

urlpatterns = [
    path('qrcode/<str:serial_no>/', spView.getQrCode, name = 'qrcode'),
    path('blank/<str:part>/<int:ordernbr>/', spView.index, name = 'blank'),
    path('post/', spView.treatStr, name='post'),
    path('template/<str:serial_no>/', spView.print_template),
    path('search/', spView.search, name='search'),
    path('', spView.history, name = 'history'),
    path('change/<int:id>/', spView.change, name='change'),
    path('update/', spView.update, name = 'update'),
    path('del/<int:record_id>/', spView.markdel, name = 'dele'),
    path('logout/', spView.logout, name = 'logout'),
    path('pbm/', spView.pbm, name = 'pbm'),
    path('getpbm/', spView.get_pbm, name = 'get_pbm'),
    path('sfmchart/', spView.sfmchart, name = 'sfm_chart'),
    path('clear/', spView.clear_temp, name = 'clear_temp'),
]