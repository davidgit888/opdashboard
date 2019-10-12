from django.contrib import admin,messages
from .models import ManHours,Assistance,AssisType, UserInfomation, BorrowType,Permissions,GroupPermissions
from django import forms
from django.urls import path
from django.http import HttpResponse
from django.shortcuts import render, redirect
import pandas as pd
import unicodecsv as csv
import json
from .constant import exclude_name

# Register your models here.
class UploadExcel(forms.Form):
    file = forms.FileField()

class ManHoursAdmin(admin.ModelAdmin):
    fields = ['contract','sfg','product_type','op','prob','username','qty','standard', 'real_time','confirmed','quote','cost_rate','date','original_group','work_group','flexible',
    'is_active']
    list_display = ('contract','sfg','product_type','op','prob','username','full_name','qty','standard', 'real_time','confirmed','date','original_group','work_group')
    search_fields = ['contract','sfg','username__username','username__last_name','date','original_group','work_group']
    date_hierarchy = 'date'
    list_filter = ('work_group', 'original_group','op')

    staff_fieldsets = (
    (('基本信息'), {'fields': ('contract','sfg','product_type','op','prob','username','qty','standard', 'real_time','confirmed','date','original_group','work_group')}),
    # (('个人信息'), {'fields': ('last_name', 'first_name', 'email')}),
    # # No permissions
    # (('重要日期'), {'fields': ('last_login', 'date_joined')}),
    # (('权限'), {'fields': ('is_active','is_staff','groups',)}),
        )
    actions = ["export_as_excel"]
    def full_name(self, obj):
        return ("%s%s" % (obj.username.last_name, obj.username.first_name))
    full_name.short_description = "姓名" 

    def export_as_excel(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields if field.name not in exclude_name ]
        # return HttpResponse(json.dumps(field_names))
        # field_names = [i for i in field_names if i not in exclude_name]
        #field_names.append('full_name')
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response,dialect='excel',encoding='GB18030')
        field_verbose_names = [field.verbose_name for field in meta.fields if field.name not in exclude_name]
        writer.writerow(field_verbose_names[1:])
        query = queryset.filter(is_active=True)
        for obj in query:
            row = writer.writerow([getattr(obj, field) for field in field_names[1:]])
           
        return response
    export_as_excel.short_description = "下载"

    def get_queryset(self, request):
        query = super(ManHoursAdmin, self).get_queryset(request)
        if request.user.id != 1:
            filtered_queryset = query.filter(is_active = True)
            return filtered_queryset
        else:
            return query
    def change_view(self, request, *args, **kwargs):
        # for non-superuser
        if not request.user.is_superuser:
            try:
                self.fieldsets = self.staff_fieldsets
                response = super(ManHoursAdmin, self).change_view(request, *args, **kwargs)
            finally:
                # Reset fieldsets to its original value
                self.fieldsets = ManHoursAdmin.fieldsets
            return response
        else:
            return super(ManHoursAdmin, self).change_view(request, *args, **kwargs)


class AssistanceAdmin(admin.ModelAdmin):
    fields = ['contract','a_type','a_category','a_subject','real_time','quote','cost_rate','standard','confirmed','b_category','b_subject','expense','work_group','original_group','username','comments','date','flexible']
    list_display = ('contract','full_name','a_type','a_category','a_subject','real_time','standard','confirmed','b_category','b_subject','work_group','original_group','username','date')
    search_fields = ['contract','a_type','a_category','a_subject','b_category','b_subject','work_group','original_group','username__username','username__last_name','date']
    date_hierarchy = 'date'
    list_filter = ('work_group', 'original_group','a_type','a_subject')

    staff_fieldsets = (
    (('基本信息'), {'fields': ('contract','a_type','a_category','a_subject','b_category','username','comments','standard', 'real_time',
        'confirmed','date','original_group','work_group','b_subject','expense')}),
    )
    actions = ["export_as_excel"]
    def full_name(self, obj):
        return ("%s%s" % (obj.username.last_name, obj.username.first_name))
    full_name.short_description = "姓名" 
    def export_as_excel(self, request, queryset):
        meta = self.model._meta
        exclude_name.append('attach')
        field_names = [field.name for field in meta.fields if field.name not in exclude_name ]
        #field_names.append('full_name')
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response,dialect='excel',encoding='GB18030')
        field_verbose_names = [field.verbose_name for field in meta.fields if field.name not in exclude_name ]
        writer.writerow(field_verbose_names[1:])
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names[1:]])
           
        return response
    export_as_excel.short_description = "下载"
    def get_queryset(self, request):
        query = super(AssistanceAdmin, self).get_queryset(request)
        if request.user.id != 1:
            filtered_queryset = query.filter(is_active = True)
            return filtered_queryset
        else:
            return query

    def change_view(self, request, *args, **kwargs):
        # for non-superuser
        if not request.user.is_superuser:
            try:
                self.fieldsets = self.staff_fieldsets
                response = super(AssistanceAdmin, self).change_view(request, *args, **kwargs)
            finally:
                # Reset fieldsets to its original value
                self.fieldsets = AssistanceAdmin.fieldsets
            return response
        else:
            return super(AssistanceAdmin, self).change_view(request, *args, **kwargs)

class AssisTypeAdmin(admin.ModelAdmin):
    fields = ['a_type','a_category','a_subject','b_category','b_subject','b_old_category','is_active','create_user']
    list_display = ('a_type','a_category','a_subject','b_category','b_subject','b_old_category','is_active')
    search_fields = ['a_type','a_category','a_subject','b_category','b_subject','b_old_category','is_active']
    staff_fieldsets = (
    (('基本信息'), {'fields': ('a_type','a_category','a_subject','b_category','b_subject','b_old_category','is_active')}),
    )

    def change_view(self, request, *args, **kwargs):
        # for non-superuser
        if not request.user.is_superuser:
            try:
                self.fieldsets = self.staff_fieldsets
                response = super(AssisTypeAdmin, self).change_view(request, *args, **kwargs)
            finally:
                # Reset fieldsets to its original value
                self.fieldsets = AssisTypeAdmin.fieldsets
            return response
        else:
            return super(AssisTypeAdmin, self).change_view(request, *args, **kwargs)

class UserInfomationAdmin(admin.ModelAdmin):
    fields = ['user_id','staff_no','duty','email','work_group','original_group','mobile','cost_rate','quote','is_active','flexible','permissions']
    list_display = ('user_id','staff_no','duty','email','work_group','original_group','mobile','is_active')
    search_fields = ['user_id__username','staff_no','duty','user_id__last_name','email','work_group__group_name','original_group','mobile','cost_rate','quote','is_active']
    filter_horizontal = ('permissions',)
    list_filter = ('work_group', 'original_group','duty')
    staff_fieldsets = ((('基本信息'), {'fields': ('user_id','staff_no','duty','email','work_group','original_group','mobile','is_active')}),)
    
    def change_view(self, request, *args, **kwargs):
        # for non-superuser
        if request.user.id not in [1,3]:
            try:
                self.fieldsets = self.staff_fieldsets
                response = super(UserInfomationAdmin, self).change_view(request, *args, **kwargs)
            finally:
                # Reset fieldsets to its original value
                self.fieldsets = UserInfomationAdmin.fieldsets
            return response
        else:
            return super(UserInfomationAdmin, self).change_view(request, *args, **kwargs)
    change_list_template = "report/upload_excel.html"

    def full_name(self, obj):
        return ("%s%s" % (obj.user_id.last_name, obj.user_id.first_name))
    full_name.short_description = "姓名" 

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('upload_excel/', self.upload_excel)
        ]
        return my_urls + urls
        return render(request, 'admin/report_excel_form.html',{
            'form':form,
        })
    def upload_excel(self,request):
        if request.method == 'POST':
            excel_file = request.FILES["file"]
            data = pd.read_excel(excel_file)
            data = data.drop_duplicates()
            data = data.fillna(0)
            try:
                for i in range(len(data)):
                    UserInfomation.objects.filter(user_id=data['id'][i]).update(staff_no=data['staff_no'][i],cost_rate=data['cost_rate'][i])
                self.message_user(request, '上传成功')
                return redirect("..")
            except Exception as e:
                # messages.error(request,'上传失败 '+str(e))
                # return redirect("..")
                pass

        form = UploadExcel()
        return render(request, 'admin/report_excel_form.html',{
            'form':form,
        })

    def get_queryset(self, request):
        query = super(UserInfomationAdmin, self).get_queryset(request)
        if request.user.id != 1:
            filtered_queryset = query.exclude(user_id__in= [1,82])
            return filtered_queryset
        else:
            return query
    def export_as_excel(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]
        #field_names.append('full_name')
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response,dialect='excel',encoding='GB18030')
        field_verbose_names = [field.verbose_name for field in meta.fields]
        writer.writerow(field_verbose_names[1:])
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names[1:]])
           
        return response
    # actions = ["export_as_excel"]

    export_as_excel.short_description = "下载"


class BorrowTypeAdmin(admin.ModelAdmin):
    fields = ['b_category','b_subject']
    list_display = ('b_category','b_subject')
    search_fields = ['b_category','b_subject']


class PermissionsAdmin(admin.ModelAdmin):
    fields = ['title','subtitle','subtitle2','url','flexible']
    list_display = ('title','subtitle','subtitle2','url','flexible')
    search_fields = ['title','subtitle','subtitle2','url','flexible']


class GroupPermissionsAdmin(admin.ModelAdmin):
    fields = ['group','permissions']
    list_display = ('group',)
    search_fields = ['group__name','permissions__title']
    filter_horizontal = ('permissions',)


# class UserPermissionsAdmin(admin.ModelAdmin):
#     fields = ['user','permissions']
#     list_display = ('user','permissions')
#     search_fields = ['user__username','permissions__title']


admin.site.register(ManHours, ManHoursAdmin)
admin.site.register(Assistance, AssistanceAdmin)
admin.site.register(AssisType, AssisTypeAdmin)
admin.site.register(UserInfomation, UserInfomationAdmin)
admin.site.register(BorrowType, BorrowTypeAdmin)
admin.site.register(Permissions, PermissionsAdmin)
# admin.site.register(UserPermissions, UserPermissionsAdmin)
admin.site.register(GroupPermissions, GroupPermissionsAdmin)