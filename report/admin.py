from django.contrib import admin
from .models import Report, OtherInfo, TypeStandard, SfmProd, Prob, Op
# Register your models here.

class ReportAdmin(admin.ModelAdmin):
    fields = ['sfg_id','type_name','op_id','prob','qty','user','standard_tiem','real_time']
    list_display = ('sfg_id','type_name','op_id','prob','qty','user','standard_tiem','real_time','date')
    search_fields = ['sfg_id','type_name','op_id','prob','qty','user','standard_tiem','real_time']

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

class OtherInfoAdmin(admin.ModelAdmin):
    fields = ['sfg_id','supportive_time','borrow_time']
    list_display = ('sfg_id','supportive_time','borrow_time')
    search_fields = ['sfg_id','supportive_time','borrow_time']

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


class TypeStandarAdmin(admin.ModelAdmin):
    fields = ['type_name','op_id','standard_time','prob_info']
    list_display = ('type_name','op_id','standard_time','prob_info')
    search_fields = ['type_name','op_id','standard_time','prob_info']

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
admin.site.register(OtherInfo, OtherInfoAdmin)
admin.site.register(TypeStandard, TypeStandarAdmin)
admin.site.register(SfmProd, SfmProdAdmin)
admin.site.register(Prob,ProbAdmin)
admin.site.register(Op,OpAdmin)