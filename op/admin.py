from django.contrib import admin, messages
from django.contrib.admin import AdminSite
# from .views import updateProductionData
from .models import InstalledCmm, DeliveredCmm, NewOrder, WaitingOrderAndInventory, InstalledEachYear
from django.urls import path
from django.http import HttpResponseRedirect
from .productionUpdate import updateProduction


class InsalledCmmAdmin(admin.ModelAdmin):
    fields = ['Year','Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    list_display = ('Year','Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec')
    search_fields = ['Year']
    # actions = ['update_data']

    change_list_template = 'op/update_changelist.html'
    # def save_model(self, rquest, obj, form, change):
    #     if 'update_data' in form.changed_data:
    #         messages.add_message(rquest, messages.INFO, 'Car has been sold')
    #     super(InsalledCmmAdmin, self).save_model(rquest, obj, form, change)
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('immortal/', self.update_data),
           
        ]
        return my_urls + urls

    def update_data(self, request):
        message = updateProduction()
        if "全部更新成功" in message:
            self.message_user(request, message)
        else:
            messages.error(request, message)
        return HttpResponseRedirect("../")

 

    # update_data.short_description='更新数据'
    
    # def get_actions(self, request):
    #     actions = super().get_actions(request)
    #     if 'delete_selected' in actions:
    #         del actions['delete_selected']
    #     return actions

class WaitingOrderAndInventoryAdmin(admin.ModelAdmin):
    fields = ['YearAndMonth','OrderQty','ShipmentQty','AuctalAssemblyQty','ToBeExcutedTendency','BackLogTendency','NetAvailableTendency','Backlog','ToBeExcutedOrder','NetAvailable']
    list_display = ('YearAndMonth','OrderQty','ShipmentQty','AuctalAssemblyQty','ToBeExcutedTendency','BackLogTendency','NetAvailableTendency','Backlog','ToBeExcutedOrder','NetAvailable')
    search_fields = ['YearAndMonth']
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
    change_list_template = 'op/update_changelist.html'
    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('immortal/', self.update_data),
           
        ]
        return my_urls + urls

    def update_data(self, request):
        message = updateProduction()
        if "全部更新成功" in message:
            self.message_user(request, message)
        else:
            messages.error(request, message)
        return HttpResponseRedirect("../")

class InstalledEachYearAdmin(admin.ModelAdmin):
    fields = ['Year','Global_A','Global_B','Global_C','Global_D','Global_EF','Explorer','Inspector_Pioneer_InspectorP_GlobalP','MH3D_Inspector454_Explorer454','Optive_Vision','Toro_ToroImage','Micro_Plus','Alpha_Apollo','Function_Pluse','Zoo_ZC','Stinger_ll','Global_Mini','Auctual_Build_Qty']
    list_display = ('Year','Global_A','Global_B','Global_C','Global_D','Global_EF','Explorer','Inspector_Pioneer_InspectorP_GlobalP','MH3D_Inspector454_Explorer454','Optive_Vision','Toro_ToroImage','Micro_Plus','Alpha_Apollo','Function_Pluse','Zoo_ZC','Stinger_ll','Global_Mini','Auctual_Build_Qty')
    search_fileds = ['Year']
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
    change_list_template = 'op/update_changelist.html'
    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('immortal/', self.update_data),
           
        ]
        return my_urls + urls

    def update_data(self, request):
        message = updateProduction()
        if "全部更新成功" in message:
            self.message_user(request, message)
        else:
            messages.error(request, message)
        return HttpResponseRedirect("../")


admin.site.register(InstalledCmm, InsalledCmmAdmin)
admin.site.register(DeliveredCmm, InsalledCmmAdmin)
admin.site.register(NewOrder, InsalledCmmAdmin)
admin.site.register(WaitingOrderAndInventory, WaitingOrderAndInventoryAdmin)
admin.site.register(InstalledEachYear, InstalledEachYearAdmin)

admin.site.site_header = "Hexagon"
admin.site.site_title = "管理页面"
admin.site.index_title = "欢迎来到管理页面"

########## duplicated ######
class ProducedAdminSite(AdminSite):
    site_header = 'Installed Admin Site'
    site_title = "Installed Admin Site"
    index_title = 'Installed Admin Site'

produced_admin_site = ProducedAdminSite(name='produced_admin')

produced_admin_site.register(InstalledCmm)
produced_admin_site.register(DeliveredCmm)
produced_admin_site.register(NewOrder)
produced_admin_site.register(WaitingOrderAndInventory)
produced_admin_site.register(InstalledEachYear)
