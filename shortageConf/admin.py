from django.contrib import admin, messages
from .models import Supplier, DeliveredTotal, Overdue, ReasonAnalysis
from op.shortageUpdate import update_shortage
from django.urls import path
from django.http import HttpResponseRedirect
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

class UserAdmin(BaseUserAdmin):
    # Hide super user for no super user's (Pre-populating data)
    # class UserAdmin(BaseUserAdmin):
    def get_queryset(self, request):
        qs = super(UserAdmin, self).get_queryset(request)
        if not request.user.is_superuser:
            return qs.filter(is_superuser=False)
        return qs

# Register your models here.
class DeliveredTotalAdmin(admin.ModelAdmin):
    fields = ['Year','Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    list_display = ('Year','Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec')
    search_fields = ['Year']

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
    change_list_template = 'op/shortage_updateList.html'
    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('immortal/', self.update_data),
           
        ]
        return my_urls + urls

    def update_data(self, request):
        message = update_shortage()
        if "全部更新成功" in message:
            self.message_user(request, message)
        else:
            messages.error(request, message)
        return HttpResponseRedirect("../")


class SupplierAdmin(admin.ModelAdmin):
    fields = ['supplier_name', 'quantity']
    list_display = ('supplier_name', 'quantity')
    search_fields = ['supplier_name']
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
    change_list_template = 'op/shortage_updateList.html'
    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
        path('immortal/', self.update_data),
           
        ]
        return my_urls + urls

    def update_data(self, request):
        message = update_shortage()
        if "全部更新成功" in message:
            self.message_user(request, message)
        else:
            messages.error(request, message)
        return HttpResponseRedirect("../")

class ReasonAnalysisAdmin(admin.ModelAdmin):
    fields = ['reason_category','quantity']
    list_display = ('reason_category','quantity')
    search_fields = ['reason_category']
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    change_list_template = 'op/shortage_updateList.html'
    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('immortal/', self.update_data),
        
        ]
        return my_urls + urls

    def update_data(self, request):
        message = update_shortage()
        if "全部更新成功" in message:
            self.message_user(request, message)
        else:
            messages.error(request, message)
        return HttpResponseRedirect("../")

class OverdueAdmin(admin.ModelAdmin):
    fields = ['category','quantity']
    list_display = ('category','quantity')
    search_fields = ['category']
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
    change_list_template = 'op/shortage_updateList.html'
    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
        path('immortal/', self.update_data),
        
    ]
        return my_urls + urls

    def update_data(self, request):
        message = update_shortage()
        if "全部更新成功" in message:
            self.message_user(request, message)
        else:
            messages.error(request, message)
        return HttpResponseRedirect("../")

admin.site.register(Supplier, SupplierAdmin)
admin.site.register(DeliveredTotal,DeliveredTotalAdmin)
admin.site.register(Overdue, OverdueAdmin)
admin.site.register(ReasonAnalysis,ReasonAnalysisAdmin)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)