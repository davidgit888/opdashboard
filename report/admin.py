
from django.contrib import admin, messages
from .models import Report, SupportiveTime, TypeStandard, SfmProd, Prob, Op,CoefficientSupport,Borrow,GroupOp,GroupPerform,SfgComments,OverTime,TraceLog,AnnualLeave,WorkGroups,UserGroups,DocType,DocInfo,MaterialApprove,MaterialGet,Material,MeterialUse,MeterialSurplus,UserInfo
from django.urls import path
from django.contrib.auth.models import User
import pandas as pd
from django import forms
from django.shortcuts import render, redirect
from django.http import HttpResponse
import unicodecsv as csv
from operator import or_
from django.db.models import Q
from functools import reduce


# Register your models here.
class UploadExcel(forms.Form):
    file = forms.FileField()

class ReportAdmin(admin.ModelAdmin):
    fields = ['sfg_id','type_name','op_id','qty','prob','user','standard_tiem','real_time', 'date','groups']
    list_display = ('sfg_id','type_name','op_id','prob','qty','user','full_name','standard_tiem','real_time','date','groups')
    search_fields = ['sfg_id','type_name','op_id__op_id','qty','user__username','standard_tiem','real_time','date','prob','groups']
    date_hierarchy = 'date'
    # def get_actions(self, request):
    #     actions = super().get_actions(request)
    #     if 'delete_selected' in actions:
    #         del actions['delete_selected']
    #     return actions
    def full_name(self, obj):
        return obj.user.last_name + obj.user.first_name
    full_name.short_description = "姓名" 
    actions = ["export_as_excel"]
    # filter the data according to group
    def get_queryset(self, request):
        query = super(ReportAdmin, self).get_queryset(request)
        user_all_permissions = []
        user = User.objects.get(id=request.user.id)
        groups = user.groups
        for i in groups.select_related():
            if '数据' in i.name:
                user_all_permissions.append(i.name)
        all_user_ids = []
        for i in range(len(user_all_permissions)):
            users = User.objects.filter(groups__name=user_all_permissions[i])
            for j in users:
                all_user_ids.append(j.id)
        all_user_ids=list(set(all_user_ids))
        filtered_query = query.filter(user__in=all_user_ids)
        return filtered_query  
    # Export csv file
    

    def export_as_excel(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]
        #field_names.append('full_name')
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response,dialect='excel',encoding='GB18030')

        writer.writerow(field_names[1:])
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names[1:]])
           
        return response


    export_as_excel.short_description = "下载"
    # def get_search_results(self, request, queryset, search_term):
    #     queryset, use_distinct = super(ReportAdmin, self).get_search_results(
    #                                            request, queryset, search_term)
    #     search_words = search_term.split(",")
    #     if search_words:
    #         q_objects = [Q(**{field + '__icontains': word})
    #                             for field in self.search_fields
    #                             for word in search_words]
    #         queryset |= self.model.objects.filter(reduce(or_, q_objects))
    #     return queryset, use_distinct

class SupportiveTimeAdmin(admin.ModelAdmin):
    fields = ['user','rest','clean_time','inside_group','outside_group','complete_machine','granite','prob',
    'shortage','plan_change','human_quality_issue_rework','item_quality_issue','human_quality_issue_repair',
    'equipment_mantainence','inventory_check','quality_check','document','conference','group_management','record','comments','date','borrow_time','borrow_name',
    'groups','vertical']
    list_display = ('full_name','rest','clean_time','inside_group','outside_group','complete_machine','granite','prob',
    'shortage','plan_change','human_quality_issue_rework','item_quality_issue','human_quality_issue_repair',
    'equipment_mantainence','inventory_check','quality_check','document','conference','group_management','record','borrow_time','borrow_name','comments',
    'date','groups','vertical')
    search_fields = ['user__username','date','groups']
    date_hierarchy = 'date'
    # def get_actions(self, request):
    #     actions = super().get_actions(request)
    #     if 'delete_selected' in actions:
    #         del actions['delete_selected']
    #     return actions
    def full_name(self, obj):
        return obj.user.last_name + obj.user.first_name
    full_name.short_description = "姓名" 

    # filter the data
    def get_queryset(self, request):
        query = super(SupportiveTimeAdmin, self).get_queryset(request)
        user_all_permissions = []
        user = User.objects.get(id=request.user.id)
        groups = user.groups
        for i in groups.select_related():
            if '数据' in i.name:
                user_all_permissions.append(i.name)
        all_user_ids = []
        for i in range(len(user_all_permissions)):
            users = User.objects.filter(groups__name=user_all_permissions[i])
            for j in users:
                all_user_ids.append(j.id)
        all_user_ids=list(set(all_user_ids))
        filtered_query = query.filter(user__in=all_user_ids)
        return filtered_query  
        
    # Export csv
    actions = ["export_as_excel"]    
    def export_as_excel(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response,dialect='excel',encoding='GB18030')

        writer.writerow(field_names[1:])


        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names[1:]])

        return response


    export_as_excel.short_description = "下载"

class TypeStandarAdmin(admin.ModelAdmin):
    fields = ['type_name','op_id','standard_time','prob_info']
    list_display = ('type_name','op_id','standard_time','prob_info')
    search_fields = ['type_name','op_id','standard_time','prob_info__prob_info']

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    
    change_list_template = "report/upload_excel.html"
    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('upload_excel/', self.upload_excel)
        ]
        return my_urls + urls
    
    actions = ["export_as_excel"]  
    
    def export_as_excel(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response,dialect='excel',encoding='utf-8')

        writer.writerow(field_names[1:])


        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names[1:]])
    
        return response
    export_as_excel.short_description = "下载"
    def upload_excel(self,request):
        if request.method == 'POST':
            excel_file = request.FILES["file"]
            data = pd.read_excel(excel_file)
            data = data.loc[:,~data.columns.str.contains('^Unnamed')]
            # data = data.dropna()
            # data = data[data['ProductNo']!='ProductNo']
            # data.index=range(len(data))
            # data['ProductNo'] = data['ProductNo'].apply(lambda x: int(x))
            data = data.fillna(0)
            try:
                
                    # a =SfmProd.objects.all()
                # try:
                #     TypeStandard.objects.all().delete()
                # except:
                #     pass
                for i in range(len(data)):
                    if data['prob'][i] != 0:

                        f_prob = Prob.objects.get(prob_info=data['prob'][i])
                        query = TypeStandard(type_name=data['product'][i],op_id=data['op'][i],prob_info=f_prob,standard_time=data['time'][i])
                        query.save()
                    else:
                        query = TypeStandard(type_name=data['product'][i],op_id=data['op'][i],standard_time=data['time'][i])
                        query.save()

                self.message_user(request, '上传成功')
                return redirect("..")
            except Exception as e:
                messages.error(request,'上传失败 '+str(e))
                return redirect("..")

        form = UploadExcel()
        
        return render(request, 'admin/report_excel_form.html',{
            'form':form,
        })


class SfmProdAdmin(admin.ModelAdmin):
    fields = ['sfg_id','type_name']
    list_display = ('sfg_id','type_name')
    search_fields = ['sfg_id','type_name']

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    change_list_template = "report/upload_excel.html"
    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('upload_excel/', self.upload_excel)
        ]
        return my_urls + urls

    def upload_excel(self,request):
        if request.method == 'POST':
            excel_file = request.FILES["file"]
            data = pd.read_excel(excel_file)
            data = data.loc[:,~data.columns.str.contains('^Unnamed')]
            data = data.dropna()
            data = data[data['ProductNo']!='ProductNo']
            data.index=range(len(data))
            #data['ProductNo'] = data['ProductNo'].apply(lambda x: int(x))
            try:
                
                    # a =SfmProd.objects.all()
                try:
                    SfmProd.objects.exclude(sfg_id__contains='小部件').delete()
                except:
                    pass
                for i in range(len(data)):
                    query = SfmProd(sfg_id=data['ProductNo'][i],type_name=data['ProductTypeName'][i])
                    query.save()
                self.message_user(request, '上传成功')
                return redirect("..")
            except Exception as e:
                messages.error(request,'上传失败 '+str(e))
                return redirect("..")

        form = UploadExcel()
        
        return render(request, 'admin/report_excel_form.html',{
            'form':form,
        })


class ProbAdmin(admin.ModelAdmin):
    # fields = ['prob_info']
    # list_display = ('prob_info')
    # search_fields = ['prob_info']

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


class OpAdmin(admin.ModelAdmin):
    fields = ['op_id','op_name']
    list_display = ('op_id','op_name')
    search_fields = ['op_id','op_name']
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


class CoefficientSupportAdmin(admin.ModelAdmin):
    fields = ['rest','clean_time','inside_group','outside_group','complete_machine','granite','prob',
    'shortage','plan_change','human_quality_issue_rework','item_quality_issue','human_quality_issue_repair',
    'equipment_mantainence','inventory_check','quality_check','document','conference','group_management','record','borrow_time','vertical']
    list_display = ('rest','clean_time','inside_group','outside_group','complete_machine','granite','prob',
    'shortage','plan_change','human_quality_issue_rework','item_quality_issue','human_quality_issue_repair',
    'equipment_mantainence','inventory_check','quality_check','document','conference','group_management','record','borrow_time','vertical')
    search_fields = ['rest']

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

class BorrowAdmin(admin.ModelAdmin):
    
    search_fields = ['borrow']

class GroupOpAdmin(admin.ModelAdmin):
    fields = ['group_name','op_id']
    list_display=('group_name','op_id')
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

class GroupPerformAdmin(admin.ModelAdmin):
    fields = ['user','natural_time','performance','standard_time','real_time','supportive_time','borrow_time','kpi','efficiency',
    'date','username','group','work_group']
    list_display=('user','natural_time','performance','standard_time','real_time','supportive_time','borrow_time','kpi','efficiency',
    'date','username','group','work_group','date_create')
    search_fields = ['user','natural_time','performance','standard_time','real_time','supportive_time','borrow_time','kpi','efficiency',
    'date','username','group','work_group']
    actions = ["export_as_excel"]  
    date_hierarchy = 'date'
    def export_as_excel(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response,dialect='excel',encoding='GB18030')

        writer.writerow(field_names[1:])


        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names[1:]])
    
        return response
    export_as_excel.short_description = "下载"

    def get_queryset(self, request):
        query = super(GroupPerformAdmin, self).get_queryset(request)
        user_all_permissions = []
        user = User.objects.get(id=request.user.id)
        groups = user.groups
        for i in groups.select_related():
            if '数据' in i.name:
                user_all_permissions.append(i.name)
        # all_user_ids = []
        # for i in range(len(user_all_permissions)):
        #     users = GroupPerform.objects.filter(groups__name=user_all_permissions[i])
        #     for j in users:
        #         all_user_ids.append(j.id)
        # all_user_ids=list(set(all_user_ids))
        
        filtered_query = query.filter(group__in=user_all_permissions)
        return filtered_query  
class SfgCommentsAdmin(admin.ModelAdmin):
    fields = ['sfg','comments']
    list_display = ('sfg','comments')
    search_fields = ['sfg','comments']

class OverTimeAdmin(admin.ModelAdmin):
    fields = ['user','over_time','over_time_type','is_paid','date','groups']
    list_display=('user','over_time','over_time_type','is_paid','date','full_name','groups')
    search_fields = ['user__username','over_time','over_time_type','is_paid','date','groups']
    date_hierarchy = 'date'
    def get_queryset(self, request):
        query = super(OverTimeAdmin, self).get_queryset(request)
        user_all_permissions = []
        user = User.objects.get(id=request.user.id)
        groups = user.groups
        for i in groups.select_related():
            if '数据' in i.name:
                user_all_permissions.append(i.name)
        all_user_ids = []
        for i in range(len(user_all_permissions)):
            users = User.objects.filter(groups__name=user_all_permissions[i])
            for j in users:
                all_user_ids.append(j.id)
        all_user_ids=list(set(all_user_ids))
        filtered_query = query.filter(user__in=all_user_ids)
        return filtered_query  
    def full_name(self, obj):
            return obj.user.last_name + obj.user.first_name
    full_name.short_description = "姓名" 
    actions = ["export_as_excel"]    
    def export_as_excel(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response,dialect='excel',encoding='GB18030')

        writer.writerow(field_names[1:])


        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names[1:]])

        return response


    export_as_excel.short_description = "下载"


class TraceLogAdmin(admin.ModelAdmin):
    fields = ['user','username','action_log','detail_message','comments']
    list_display = ('user','username','action_log','detail_message','comments','date')
    search_fields = ['user','username','action_log','detail_message','comments','date']


class AnnualLeaveAdmin(admin.ModelAdmin):
    fields = ['user','leave_type','start_date','end_date','hours','remarks']
    list_display = ('user','leave_type','start_date','end_date','hours','remarks')
    search_fields = ['user','leave_type','start_date','end_date','hours','remarks']

    change_list_template = "report/upload_excel.html"
    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('upload_excel/', self.upload_excel)
        ]
        return my_urls + urls

    def upload_excel(self,request):
        if request.method == 'POST':
            excel_file = request.FILES["file"]
            data = pd.read_excel(excel_file,sheet_name='已审批休假')
            # data = data.loc[:,~data.columns.str.contains('^Unnamed')]
            # data = data.dropna()
            # data = data[data['ProductNo']!='ProductNo']
            # data.index=range(len(data))
            # data['ProductNo'] = data['ProductNo'].apply(lambda x: int(x))
            # data = data.fillna(0)
            try:
                
                    # a =SfmProd.objects.all()
                # try:
                #     TypeStandard.objects.all().delete()
                # except:
                #     pass
                for i in range(len(data)):

                    query = AnnualLeave(user=data['Staff_Name'][i],leave_type=data['Leave_Description'][i],start_date=data['Start_Date'][i],
                        end_date= data['End_Date'][i],hours =data['Apply_Nums'][i] ,remarks=data['Remarks'][i])
                    query.save()

                self.message_user(request, '上传成功')
                return redirect("..")
            except Exception as e:
                messages.error(request,'上传失败 '+str(e))
                return redirect("..")

        form = UploadExcel()
        
        return render(request, 'admin/report_excel_form.html',{
            'form':form,
        })
    
class UserGroupsAdmin(admin.ModelAdmin):
    fields = ['user','work_group']
    list_display = ('user','full_name','work_group')
    search_fields = ['user__username','work_group__group_name']
    def full_name(self, obj):
        return obj.user.last_name + obj.user.first_name

class WorkGroupsAdmin(admin.ModelAdmin):
    fields = ['group_name']
    list_display = ('group_name',)
    search_fields = ['group_name']

class DocTypeAdmin(admin.ModelAdmin):
    fields = ['type','type_id']
    list_display = ('type','type_id')
    search_fields = ['type','type_id']

class DocInfoAdmin(admin.ModelAdmin):
    fields = ['sfg','type','info']
    list_display = ('sfg','type','info','date')
    search_fields = ['sfg','type__type','info']


class MaterialAdmin(admin.ModelAdmin):
    fields = ['sno','name','unit','attribute','comments','price']
    list_display = ('sno','name','unit','attribute','comments','price')
    search_fields = ['sno','name','unit','attribute','comments','price']
    
    change_list_template = "report/upload_excel.html"
    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('upload_excel/', self.upload_excel)
        ]
        return my_urls + urls

    def upload_excel(self,request):
        if request.method == 'POST':
            excel_file = request.FILES["file"]
            data = pd.read_excel(excel_file)
            data['price'] = data['price'].round(2)
            #data['ProductNo'] = data['ProductNo'].apply(lambda x: int(x))
            try:
                
                    # a =SfmProd.objects.all()
                try:
                    Material.objects.all().delete()
                except:
                    return HttpResponse('cannot delete all')
                for i in range(len(data)):
                    query = Material(sno=data['ID'][i],name=data['name'][i],unit=data['unit'][i],
                        attribute=data['type'][i],comments=data['yon'][i],price=data['price'][i])
                    query.save()
                self.message_user(request, '上传成功')
                return redirect("..")
            except Exception as e:
                messages.error(request,'上传失败 '+str(e))
                return redirect("..")

        form = UploadExcel()
        
        return render(request, 'admin/report_excel_form.html',{
            'form':form,
        })

class MaterialApproveAdmin(admin.ModelAdmin):
    fields = ['sno','year','quarter','group','user','qty','qty_request','qty_sup','qty_get']
    list_display = ('sno','year','quarter','group','user','qty','date','qty_request','qty_sup','qty_get')
    search_fields = ['sno__sno','year','quarter','group__group_name','user__username','qty','date']

class MaterialGetAdmin(admin.ModelAdmin):
    fields = ['sno','year','quarter','group','user','qty']
    list_display = ('sno','year','quarter','group','user','qty','date')
    search_fields = ['sno','year','quarter','group','user','qty','date']

class MeterialUseAdmin(admin.ModelAdmin):
    fields = ['sno','year','quarter','group','user','qty']
    list_display = ('sno','year','quarter','group','user','qty','date')
    search_fields = ['sno__sno','year','quarter','group__group_name','user__username','qty','date']

class MeterialSurplusAdmin(admin.ModelAdmin):
    fields = ['sno','year','quarter','group','user','qty']
    list_display = ('sno','year','quarter','group','user','qty','date')
    search_fields = ['sno__sno','year','quarter','group__group_name','user__username','qty','date']

class UserInfoAdmin(admin.ModelAdmin):
    """docstring for UserInfoAdmin"""
    fields = ['user_id','staff_no','duty','email','work_group','department','mobile']
    list_display = ('user_id','staff_no','duty','email','work_group','department','mobile')
    search_fields = ['user_id__username','staff_no','duty','email','work_group__group_name','department','mobile']


    
        

admin.site.register(Report, ReportAdmin)
admin.site.register(SupportiveTime, SupportiveTimeAdmin)
admin.site.register(TypeStandard, TypeStandarAdmin)
admin.site.register(SfmProd, SfmProdAdmin)
admin.site.register(Prob,ProbAdmin)
admin.site.register(Op,OpAdmin)
admin.site.register(CoefficientSupport,CoefficientSupportAdmin)
admin.site.register(Borrow,BorrowAdmin)
admin.site.register(GroupOp,GroupOpAdmin)
admin.site.register(GroupPerform,GroupPerformAdmin)
admin.site.register(SfgComments,SfgCommentsAdmin)
admin.site.register(OverTime,OverTimeAdmin)
admin.site.register(TraceLog,TraceLogAdmin)
admin.site.register(AnnualLeave,AnnualLeaveAdmin)
admin.site.register(UserGroups,UserGroupsAdmin)
admin.site.register(WorkGroups,WorkGroupsAdmin)
admin.site.register(DocType, DocTypeAdmin)
admin.site.register(DocInfo,DocInfoAdmin)
admin.site.register(Material,MaterialAdmin)
admin.site.register(MaterialApprove,MaterialApproveAdmin)
admin.site.register(MaterialGet,MaterialGetAdmin)
admin.site.register(MeterialUse,MeterialUseAdmin)
admin.site.register(MeterialSurplus,MeterialSurplusAdmin)
admin.site.register(UserInfo,UserInfoAdmin)