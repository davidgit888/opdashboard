
from django.contrib import admin, messages
from .models import Report, SupportiveTime, TypeStandard, SfmProd, Prob, Op,CoefficientSupport,Borrow,GroupOp
from django.urls import path
from django.contrib.auth.models import User
import pandas as pd
from django import forms
from django.shortcuts import render, redirect
from django.http import HttpResponse
import unicodecsv as csv

# Register your models here.
class UploadExcel(forms.Form):
    file = forms.FileField()

class ReportAdmin(admin.ModelAdmin):
    fields = ['sfg_id','type_name','op_id','qty','prob','user','standard_tiem','real_time','date']
    list_display = ('sfg_id','type_name','op_id','prob','qty','user','full_name','standard_tiem','real_time','date')
    search_fields = ['sfg_id','type_name','op_id__op_id','qty','user__username','standard_tiem','real_time','date','prob']

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
    def full_name(self, obj):
        return obj.user.last_name + obj.user.first_name
    full_name.short_description = "姓名" 
    
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
    actions = ["export_as_excel"]

    def export_as_excel(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]
        #field_names.append('full_name')
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response,dialect='excel',encoding='gb2312')

        writer.writerow(field_names[1:])
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names[1:]])
            # sfg_id = getattr(obj,field_names[1])
            # if not sfg_id:
            #     sfg_id = ' '
            # type_name = getattr(obj, field_names[2])
            # type_name = type_name + ' '
            # if not type_name:
            #     type_name = ' '
            
            # op_id = getattr(obj,field_names[3])
            # op_id = str(op_id) + ' '
            # if not op_id:
            #     op_id = ' '
            
            # prob = getattr(obj,field_names[4])
            # #prob = prob + ' '
            # if not prob:
            #     prob = 'No'
            
            # qty = getattr(obj, field_names[5])
            # if not qty:
            #     qty = ' '
            
            # user = getattr(obj, field_names[6])
            # if not user:
            #     user = ' '

            # standard_time = getattr(obj, field_names[7])
            # if not standard_time:
            #     standard_time = ' '

            # real_time = getattr(obj, field_names[8])
            # if not real_time:
            #     real_time = ' '

            # date = getattr(obj, field_names[9])
            # if not date:
            #     date = ' '

            # row = writer.writerow([sfg_id,type_name, op_id, prob, qty, user, standard_time,real_time,date])
        return response


    export_as_excel.short_description = "下载"

class SupportiveTimeAdmin(admin.ModelAdmin):
    fields = ['user','rest','clean_time','inside_group','outside_group','complete_machine','granite','prob',
    'shortage','plan_change','human_quality_issue_rework','item_quality_issue','human_quality_issue_repair',
    'equipment_mantainence','inventory_check','quality_check','document','conference','group_management','record','comments','date','borrow_time','borrow_name']
    list_display = ('user','rest','clean_time','inside_group','outside_group','complete_machine','granite','prob',
    'shortage','plan_change','human_quality_issue_rework','item_quality_issue','human_quality_issue_repair',
    'equipment_mantainence','inventory_check','quality_check','document','conference','group_management','record','borrow_time','borrow_name','comments','date')
    search_fields = ['user__username','date']

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

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
        writer = csv.writer(response,dialect='excel',encoding='gb2312')

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

    def upload_excel(self,request):
        if request.method == 'POST':
            excel_file = request.FILES["file"]
            data = pd.read_excel(excel_file)
            data = data.loc[:,~data.columns.str.contains('^Unnamed')]
            data = data.dropna()
            data = data[data['ProductNo']!='ProductNo']
            data.index=range(len(data))
            data['ProductNo'] = data['ProductNo'].apply(lambda x: int(x))
            data = data.fillna(0)
            try:
                
                    # a =SfmProd.objects.all()
                try:
                    TypeStandard.objects.all().delete()
                except:
                    pass
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
    'equipment_mantainence','inventory_check','quality_check','document','conference','group_management','record','borrow_time']
    list_display = ('rest','clean_time','inside_group','outside_group','complete_machine','granite','prob',
    'shortage','plan_change','human_quality_issue_rework','item_quality_issue','human_quality_issue_repair',
    'equipment_mantainence','inventory_check','quality_check','document','conference','group_management','record','borrow_time')
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


admin.site.register(Report, ReportAdmin)
admin.site.register(SupportiveTime, SupportiveTimeAdmin)
admin.site.register(TypeStandard, TypeStandarAdmin)
admin.site.register(SfmProd, SfmProdAdmin)
admin.site.register(Prob,ProbAdmin)
admin.site.register(Op,OpAdmin)
admin.site.register(CoefficientSupport,CoefficientSupportAdmin)
admin.site.register(Borrow,BorrowAdmin)
admin.site.register(GroupOp,GroupOpAdmin)