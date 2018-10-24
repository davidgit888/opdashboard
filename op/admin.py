from django.contrib import admin

from django.contrib import admin
from .models import InstalledCmm, DeliveredCmm, NewOrder, WaitingOrderAndInventory, InstalledEachYear

class InsalledCmmAdmin(admin.ModelAdmin):
    fields = ['Year','Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    list_display = ('Year','Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec')
    search_fields = ['Year']

class WaitingOrderAndInventoryAdmin(admin.ModelAdmin):
    fields = ['YearAndMonth','OrderQty','ShipmentQty','AuctalAssemblyQty','ToBeExcutedTendency','BackLogTendency','NetAvailableTendency','Backlog','ToBeExcutedOrder','NetAvailable']
    list_display = ('YearAndMonth','OrderQty','ShipmentQty','AuctalAssemblyQty','ToBeExcutedTendency','BackLogTendency','NetAvailableTendency','Backlog','ToBeExcutedOrder','NetAvailable')
    search_fields = ['YearAndMonth']

class InstalledEachYearAdmin(admin.ModelAdmin):
    fields = ['Year','Global_A','Global_B','Global_C','Global_D','Global_EF','Explorer','Inspector_Pioneer_InspectorP_GlobalP','MH3D_Inspector454_Explorer454','Optive_Vision','Toro_ToroImage','Micro_Plus','Alpha_Apollo','Function_Pluse','Zoo_ZC','Stinger_ll','Global_Mini','Auctual_Build_Qty']
    list_display = ('Year','Global_A','Global_B','Global_C','Global_D','Global_EF','Explorer','Inspector_Pioneer_InspectorP_GlobalP','MH3D_Inspector454_Explorer454','Optive_Vision','Toro_ToroImage','Micro_Plus','Alpha_Apollo','Function_Pluse','Zoo_ZC','Stinger_ll','Global_Mini','Auctual_Build_Qty')
    search_fileds = ['Year']

admin.site.register(InstalledCmm, InsalledCmmAdmin)
admin.site.register(DeliveredCmm, InsalledCmmAdmin)
admin.site.register(NewOrder, InsalledCmmAdmin)
admin.site.register(WaitingOrderAndInventory, WaitingOrderAndInventoryAdmin)
admin.site.register(InstalledEachYear, InstalledEachYearAdmin)
admin.site.site_header = "Hexagon"
admin.site.site_title = "管理页面"
admin.site.index_title = "欢迎来到管理页面"
