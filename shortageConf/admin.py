from django.contrib import admin
from .models import Supplier, DeliveredTotal, Overdue, ReasonAnalysis
# Register your models here.
class DeliveredTotalAdmin(admin.ModelAdmin):
    fields = ['Year','Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    list_display = ('Year','Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec')
    search_fields = ['Year']

class SupplierAdmin(admin.ModelAdmin):
    fields = ['supplier_name', 'quantity']
    list_display = ('supplier_name', 'quantity')
    search_fields = ['supplier_name']

class ReasonAnalysisAdmin(admin.ModelAdmin):
    fields = ['reason_category','quantity']
    list_display = ('reason_category','quantity')
    search_fields = ['reason_category']

class OverdueAdmin(admin.ModelAdmin):
    fields = ['category','quantity']
    list_display = ('category','quantity')
    search_fields = ['category']

admin.site.register(Supplier, SupplierAdmin)
admin.site.register(DeliveredTotal,DeliveredTotalAdmin)
admin.site.register(Overdue, OverdueAdmin)
admin.site.register(ReasonAnalysis,ReasonAnalysisAdmin)