from django.db import models


class InstalledCmm(models.Model):
    Year = models.CharField(max_length=5)
    Jan = models.IntegerField(null=True, blank=True)
    Feb = models.IntegerField(null=True, blank=True)
    Mar = models.IntegerField(null=True, blank=True)
    Apr = models.IntegerField(null=True, blank=True)
    May = models.IntegerField(null=True, blank=True)
    Jun = models.IntegerField(null=True, blank=True)
    Jul = models.IntegerField(null=True, blank=True)
    Aug = models.IntegerField(null=True, blank=True)
    Sep = models.IntegerField(null=True, blank=True)
    Oct = models.IntegerField(null=True, blank=True)
    Nov = models.IntegerField(null=True, blank=True)
    Dec = models.IntegerField(null=True, blank=True)
    class Meta:
        verbose_name = '生产装机数量统计'
        verbose_name_plural = '生产装机数量统计'

    def __str__(self):
        return '%s %s %s %s %s %s %s %s %s %s %s %s %s' % (self.Year, self.Jan, self.Feb, self.Mar, self.Apr, self.May,self.Jun, self.Jul,
                self.Aug, self.Sep, self.Oct, self.Nov, self.Dec)
    # actions = ['update_data']
    # def update_data(self, request, queryset):
    #     print('<p>Hello</p>')
    # update_data.short_description='Applying'
class DeliveredCmm(models.Model):
    Year = models.CharField(max_length=5, null=True, blank=True)
    Jan = models.IntegerField(null=True, blank=True)
    Feb = models.IntegerField(null=True, blank=True)
    Mar = models.IntegerField(null=True, blank=True)
    Apr = models.IntegerField(null=True, blank=True)
    May = models.IntegerField(null=True, blank=True)
    Jun = models.IntegerField(null=True, blank=True)
    Jul = models.IntegerField(null=True, blank=True)
    Aug = models.IntegerField(null=True, blank=True)
    Sep = models.IntegerField(null=True, blank=True)
    Oct = models.IntegerField(null=True, blank=True)
    Nov = models.IntegerField(null=True, blank=True)
    Dec = models.IntegerField(null=True, blank=True)
    class Meta:
        verbose_name = '生产发货量统计'
        verbose_name_plural = '生产发货量统计'

    # def __str__(self):
    #     return (self.Year, self.Jan, self.Feb, self.Mar, self.Apr, self.May,self.Jun, self.Jul,
    #             self.Aug, self.Sep, self.Oct, self.Nov, self.Dec)

class NewOrder(models.Model):
    Year = models.CharField(max_length=4,null=True, blank=True)
    Jan = models.IntegerField(null=True, blank=True)
    Feb = models.IntegerField(null=True, blank=True)
    Mar = models.IntegerField(null=True, blank=True)
    Apr = models.IntegerField(null=True, blank=True)
    May = models.IntegerField(null=True, blank=True)
    Jun = models.IntegerField(null=True, blank=True)
    Jul = models.IntegerField(null=True, blank=True)
    Aug = models.IntegerField(null=True, blank=True)
    Sep = models.IntegerField(null=True, blank=True)
    Oct = models.IntegerField(null=True, blank=True)
    Nov = models.IntegerField(null=True, blank=True)
    Dec = models.IntegerField(null=True, blank=True)
    class Meta:
        verbose_name = '新进生产订单数量汇总'
        verbose_name_plural = '新进生产订单数量汇总'
    # def __str__(self):
    #     return (self.Year, self.Jan, self.Feb, self.Mar, self.Apr, self.May,self.Jun, self.Jul,
    #             self.Aug, self.Sep, self.Oct, self.Nov, self.Dec)

class WaitingOrderAndInventory(models.Model):
    YearAndMonth = models.CharField(max_length=7,null=True, blank=True)
    OrderQty = models.IntegerField(null=True, blank=True)
    ShipmentQty = models.IntegerField(null=True, blank=True)
    AuctalAssemblyQty = models.IntegerField(null=True, blank=True)
    ToBeExcutedTendency = models.IntegerField(null=True, blank=True)
    BackLogTendency = models.IntegerField(null=True, blank=True)
    NetAvailableTendency = models.IntegerField(null=True, blank=True)
    Backlog = models.IntegerField(null=True, blank=True)
    ToBeExcutedOrder = models.IntegerField(null=True, blank=True)
    NetAvailable = models.IntegerField(null=True, blank=True)
    class Meta:
        verbose_name = '整机“待执行订单” & “证据库存” 数据汇总'
        verbose_name_plural = '整机“待执行订单” & “整机库存” 数据汇总'

class InstalledEachYear(models.Model):
    Year = models.CharField(max_length=4,null=True, blank=True)
    Global_A = models.IntegerField(null=True, blank=True)
    Global_B = models.IntegerField(null=True, blank=True)
    Global_C = models.IntegerField(null=True, blank=True)
    Global_D = models.IntegerField(null=True, blank=True)
    Global_EF = models.IntegerField(null=True, blank=True)
    Explorer = models.IntegerField(null=True, blank=True)
    Inspector_Pioneer_InspectorP_GlobalP = models.IntegerField(null=True, blank=True)
    MH3D_Inspector454_Explorer454 = models.IntegerField(null=True, blank=True)
    Optive_Vision = models.IntegerField(null=True, blank=True)
    Toro_ToroImage = models.IntegerField(null=True, blank=True)
    Micro_Plus = models.IntegerField(null=True, blank=True)
    Alpha_Apollo= models.IntegerField(null=True, blank=True)
    Function_Pluse = models.IntegerField(null=True, blank=True)
    Zoo_ZC = models.IntegerField(null=True, blank=True)
    Stinger_ll = models.IntegerField(null=True, blank=True)
    Global_Mini = models.IntegerField(null=True, blank=True)
    Auctual_Build_Qty = models.IntegerField(null=True, blank=True)
    class Meta:
        verbose_name = '历年生产装机量汇总'
        verbose_name_plural = '历年生产装机量汇总'
    
