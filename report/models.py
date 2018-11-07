from django.db import models
from django.contrib.auth.models import User
from datetime import date
# Create your models here.
class SfmProd(models.Model):
    sfg_id = models.CharField(max_length=15, verbose_name='SFG',default='')
    type_name = models.CharField(max_length=30, verbose_name='机型')
    class Meta:
        verbose_name = 'SFM信息'
        verbose_name_plural = 'SFM信息'
    def __str__(self):
    
        return '%s %s' % (self.sfg_id, self.type_name)

class Prob(models.Model):
    prob_info = models.CharField(max_length=20,  verbose_name='测针信息')
    class Meta:
        verbose_name = "测头信息"
        verbose_name_plural = "测头信息"
    def __str__(self):
        
        return '%s' % (self.prob_info)
class TypeStandard(models.Model):
    type_name = models.CharField(max_length=30,verbose_name='机型')
    op_id = models.IntegerField( verbose_name='工步')
    prob_info = models.ForeignKey(Prob, verbose_name='测头信息',db_column='prob_info',on_delete=models.CASCADE,null=True, blank=True)
    standard_time = models.CharField(verbose_name='标准工时',max_length=10)
    class Meta:
        verbose_name = '标准工时'
        verbose_name_plural = '标准工时'



    def __str__(self):
        return '%s' % (self.prob_info)

class Op(models.Model):
    op_id = models.IntegerField()
    op_name = models.CharField(max_length=5)
    class Meta:
        verbose_name = "工步信息"
        verbose_name_plural = "工步信息"

    def __str__(self):
        return '%s %s' % (self.op_id, self.op_name)  

 


class Report(models.Model):
    # sfg_id = models.ForeignKey(SfmProd, db_column='sfg_id', related_name='sfmprod_sfgid',on_delete=models.CASCADE)
    sfg_id = models.CharField(max_length=15, verbose_name='SFG',default='')
    type_name = models.CharField(max_length=20,default='',verbose_name='机型')
    op_id = models.ForeignKey(Op, db_column='op_id',on_delete=models.CASCADE,verbose_name='工步')
    prob = models.CharField(max_length=20,default='',verbose_name='测头')
    qty = models.FloatField(max_length=4, default=1,verbose_name='数量')
    #user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default='',verbose_name='用户名')
    standard_tiem = models.FloatField(max_length=4,verbose_name='标准工时')
    real_time = models.FloatField(verbose_name='实际工时',max_length=4,default='')
    date = models.DateField(auto_now=False,default=date.today())
    def __str__(self):
        return '%s %s %s %s  %s  %s  %s  %s  %s ' % (self.sfg_id, self.type_name, self.op_id, self.prob,self.qty,self.user,self.standard_tiem,self.real_time,self.date)
    class Meta:
        verbose_name = '报工平台'
        verbose_name_plural = '报工平台'

class SupportiveTime(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户')
    rest = models.FloatField(verbose_name='休息',max_length=10,null=True, default=0, blank=True)
    clean_time = models.FloatField(verbose_name='卫生',max_length=10,null=True, default=0, blank=True)
    inside_group = models.FloatField(verbose_name='组内',max_length=10,null=True, default=0, blank=True)
    outside_group = models.FloatField(verbose_name='组外',max_length=10,null=True, default=0, blank=True)
    complete_machine = models.FloatField(verbose_name='整机',max_length=10,null=True, default=0, blank=True)
    granite = models.FloatField(verbose_name='花岗石',max_length=10,null=True, default=0, blank=True)
    prob = models.FloatField(verbose_name='测头',max_length=10,null=True, default=0, blank=True)
    shortage = models.FloatField(verbose_name='补缺件',max_length=10,null=True, default=0, blank=True)
    plan_change = models.FloatField(verbose_name='计划调整',max_length=10,null=True, default=0, blank=True)
    human_quality_issue_rework = models.FloatField(verbose_name='人为质量问题返工',max_length=10,null=True, default=0, blank=True)
    item_quality_issue = models.FloatField(verbose_name='零件质量问题',max_length=10,null=True, default=0, blank=True)
    human_quality_issue_repair = models.FloatField(verbose_name='人为质量问题返修',max_length=10,null=True, default=0, blank=True)
    equipment_mantainence = models.FloatField(verbose_name='设备维护',max_length=10,null=True, default=0, blank=True)
    inventory_check =models.FloatField(verbose_name='库存核查',max_length=10,null=True, default=0, blank=True)
    quality_check = models.FloatField(verbose_name='质量审核',max_length=10,null=True, default=0, blank=True)
    document = models.FloatField(verbose_name='档案整理',max_length=10,null=True, default=0, blank=True)
    conference = models.FloatField(verbose_name='会议',max_length=10,null=True, default=0, blank=True)
    group_management = models.FloatField(verbose_name='班组管理',max_length=10,null=True, default=0, blank=True)
    record = models.FloatField(verbose_name='记录',max_length=10,null=True, default=0, blank=True)
    date = models.DateField(auto_now=False,verbose_name='日期',default=date.today())
    
    def __str__(self):
        return '%s ' % (self.date)
    class Meta:
        verbose_name = '辅助工时'
        verbose_name_plural = '辅助工时'

# class SupportTime(models.Model):
    
#     rest = models.FloatField(max_length=4,verbose_name='标准工时',null=True)
#     clean = models.CharField(max_length=4,verbose_name='标准工时',null=True)
#     inside_group = models.FloatField(max_length=4,verbose_name='标准工时',null=True)
#     outside_group = models.FloatField(max_length=4,verbose_name='标准工时',null=True)
#     complete_machine = models.FloatField(max_length=4,verbose_name='标准工时',null=True)
#     granite = models.FloatField(max_length=4,verbose_name='标准工时',null=True)
#     prob = models.FloatField(max_length=4,verbose_name='标准工时',null=True)
#     shortage = models.FloatField(max_length=4,verbose_name='标准工时',null=True)
#     plan_change = models.FloatField(max_length=4,verbose_name='标准工时',null=True)
#     human_quality_issue_rework = models.FloatField(max_length=4,verbose_name='标准工时',null=True)
#     item_quality_issue = models.FloatField(max_length=4,verbose_name='标准工时',null=True)
#     human_quality_issue_repair = models.FloatField(max_length=4,verbose_name='标准工时',null=True)
#     equipment_mantainence = models.FloatField(max_length=4,verbose_name='标准工时',null=True)
#     inventory_check = models.FloatField(max_length=4,verbose_name='标准工时',null=True)
#     quality_check = models.FloatField(max_length=4,verbose_name='标准工时',null=True)
#     document = models.FloatField(max_length=4,verbose_name='标准工时',null=True)
#     conference = models.FloatField(max_length=4,verbose_name='标准工时',null=True)
#     group_management = models.FloatField(max_length=4,verbose_name='标准工时',null=True)
#     record = models.FloatField(max_length=4,verbose_name='标准工时',null=True)
#     date = models.DateField(auto_now=True)
#     user = models.ForeignKey(User, on_delete=models.CASCADE, default='',verbose_name='用户名')

    
#     date = models.DateField(auto_now=True)
#     class Meta:
#         verbose_name = '辅助工时1'
#         verbose_name_plural = '辅助工时1'








