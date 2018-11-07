
from django.contrib import admin, messages
from .models import Report, SupportiveTime, TypeStandard, SfmProd, Prob, Op
from django.urls import path
import pandas as pd
from django import forms
from django.shortcuts import render, redirect
# Register your models here.
class UploadExcel(forms.Form):
    file = forms.FileField()

class ReportAdmin(admin.ModelAdmin):
    fields = ['sfg_id','type_name','op_id','prob','qty','user','standard_tiem','real_time','date']
    list_display = ('sfg_id','type_name','op_id','prob','qty','user','standard_tiem','real_time','date')
    search_fields = ['sfg_id','type_name','op_id__op_id','prob','qty','user__username','standard_tiem','real_time','date']

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

class SupportiveTimeAdmin(admin.ModelAdmin):
    fields = ['user','rest','clean_time','inside_group','outside_group','complete_machine','granite','prob',
    'shortage','plan_change','human_quality_issue_rework','item_quality_issue','human_quality_issue_repair',
    'equipment_mantainence','inventory_check','quality_check','document','conference','group_management','record','date']
    list_display = ('user','rest','clean_time','inside_group','outside_group','complete_machine','granite','prob',
    'shortage','plan_change','human_quality_issue_rework','item_quality_issue','human_quality_issue_repair',
    'equipment_mantainence','inventory_check','quality_check','document','conference','group_management','record','date')
    search_fields = ['user__username']

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


class TypeStandarAdmin(admin.ModelAdmin):
    fields = ['type_name','op_id','standard_time','prob_info']
    list_display = ('type_name','op_id','standard_time','prob_info')
    search_fields = ['type_name','op_id','standard_time','prob_info__prob_info']

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


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
            data['ProductNo'] = data['ProductNo'].apply(lambda x: int(x))
            try:
                
                    # a =SfmProd.objects.all()
                try:
                    SfmProd.objects.all().delete()
                except:
                    pass
                for i in range(len(data)):
                    query = SfmProd(sfg_id=data['ProductNo'][i],type_name=data['ProductTypeName'][i])
                    query.save()
                self.message_user(request, '上产成功')
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




admin.site.register(Report, ReportAdmin)
admin.site.register(SupportiveTime, SupportiveTimeAdmin)
admin.site.register(TypeStandard, TypeStandarAdmin)
admin.site.register(SfmProd, SfmProdAdmin)
admin.site.register(Prob,ProbAdmin)
admin.site.register(Op,OpAdmin)