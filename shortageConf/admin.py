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
    list_display = ('username','email','last_name','first_name','is_staff','is_active')
    def get_queryset(self, request):
        qs = super(UserAdmin, self).get_queryset(request)
        if not request.user.is_superuser:
            return qs.filter(is_superuser=False)
        return qs
    # hide is_superuser if user is not superuser
    staff_fieldsets = (
    (('用户名'), {'fields': ('username', 'password')}),
    (('个人信息'), {'fields': ('last_name', 'first_name', 'email')}),
    # No permissions
    (('重要日期'), {'fields': ('last_login', 'date_joined')}),
    (('权限'), {'fields': ('is_active','is_staff','groups',)}),
        )
    def get_queryset(self, request):
        query = super(UserAdmin, self).get_queryset(request)
        user_all_permissions = []
        user = User.objects.get(id=request.user.id)
        groups = user.groups
        permission_check=0
        for i in groups.select_related():
            if '数据' in i.name:
                user_all_permissions.append(i.name)
            if '主管' in i.name:
                permission_check = 1
            
        all_user_ids = []
        for i in range(len(user_all_permissions)):
            users = User.objects.filter(groups__name=user_all_permissions[i])
            for j in users:
                all_user_ids.append(j.id)
        all_user_ids=list(set(all_user_ids))
        # filter admin
        if request.user.is_superuser:
            # filtered_query = query.filter(id__in=all_user_ids)
            return query
        elif permission_check==1:
            return query.exclude(id=1)
        else:
            filtered_query = query.filter(id__in=all_user_ids).exclude(id=1)
        return filtered_query  
    
    def change_view(self, request, *args, **kwargs):
        # for non-superuser
        if not request.user.is_superuser:
            try:
                self.fieldsets = self.staff_fieldsets
                response = super(UserAdmin, self).change_view(request, *args, **kwargs)
            finally:
                # Reset fieldsets to its original value
                self.fieldsets = UserAdmin.fieldsets
            return response
        else:
            return super(UserAdmin, self).change_view(request, *args, **kwargs)

    



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