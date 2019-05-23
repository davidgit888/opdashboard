from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import auth
# Create your views here.
def index(request):
    return render(request, 'op/login.html')

#@login_required(login_url='/accounts/login/')
def loginAuth(request):
    return HttpResponseRedirect('op/dashboard/')

def loggedout(request):
    auth.logout(request)
    return render(request, 'op/login.html', {
        'error_message':'You have successfully logged out'
    })