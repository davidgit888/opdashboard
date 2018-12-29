from django.db import models
from django.contrib.auth.models import User
from datetime import date
from django.utils.timezone import now
# Create your models here.
class SfmProd(models.Model):
    sfg_id = models.CharField(max_length=15, verbose_name='SFG',default='')
    type_name = models.CharField(max_length=50, verbose_name='机型')
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
    type_name = models.CharField(max_length=50,verbose_name='机型')
    op_id = models.IntegerField( verbose_name='工步')
    prob_info = models.ForeignKey(Prob, verbose_name='测头信息',db_column='prob_info',on_delete=models.CASCADE,null=True, blank=True)
    standard_time = models.CharField(verbose_name='标准工时',max_length=20)
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
    
    sfg_id = models.CharField(max_length=15, verbose_name='SFG',default='')
    type_name = models.CharField(max_length=50,default='',verbose_name='机型')
    op_id = models.ForeignKey(Op, db_column='op_id',on_delete=models.CASCADE,verbose_name='工步')
    prob = models.CharField(max_length=20,default='',verbose_name='测头',null=True, blank=True)
    qty = models.FloatField(max_length=4, default=1,verbose_name='数量')
    
    user = models.ForeignKey(User, related_name="user_full_name", on_delete=models.CASCADE, default='',verbose_name='用户名')
    standard_tiem = models.FloatField(max_length=4,verbose_name='标准工时')
    real_time = models.FloatField(verbose_name='实际工时',max_length=4,default='')

    date = models.DateField(auto_now=False,default=date.today())
    date_time = models.DateTimeField(auto_created=True,verbose_name='提交时间',default=now())
    groups = models.CharField(max_length=20,default='',verbose_name='班组')
    def __str__(self):
        return '%s %s %s %s  %s  %s  %s  %s  %s %s' % (self.sfg_id, self.type_name, self.op_id, self.prob,self.qty,self.user,self.standard_tiem,self.real_time,self.date,self.groups)
    class Meta:
        verbose_name = '制造工时'
        verbose_name_plural = '制造工时'

class SupportiveTime(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户')
    rest = models.FloatField(verbose_name='休息',max_length=10, default=0)
    clean_time = models.FloatField(verbose_name='卫生',max_length=10, default=0)
    inside_group = models.FloatField(verbose_name='组内',max_length=10, default=0)
    outside_group = models.FloatField(verbose_name='组外',max_length=10, default=0)
    complete_machine = models.FloatField(verbose_name='整机',max_length=10, default=0)
    granite = models.FloatField(verbose_name='花岗石',max_length=10, default=0)
    prob = models.FloatField(verbose_name='物流搬运',max_length=10, default=0)
    shortage = models.FloatField(verbose_name='补缺件',max_length=10, default=0)
    plan_change = models.FloatField(verbose_name='计划调整',max_length=10, default=0)
    human_quality_issue_rework = models.FloatField(verbose_name='人为质量问题返工',max_length=10, default=0)
    item_quality_issue = models.FloatField(verbose_name='零件质量问题',max_length=10, default=0)
    human_quality_issue_repair = models.FloatField(verbose_name='人为质量问题返修',max_length=10, default=0)
    equipment_mantainence = models.FloatField(verbose_name='设备维护',max_length=10, default=0)
    inventory_check =models.FloatField(verbose_name='库存核查',max_length=10, default=0)
    quality_check = models.FloatField(verbose_name='质量审核',max_length=10,default=0)
    document = models.FloatField(verbose_name='档案整理',max_length=10, default=0)
    conference = models.FloatField(verbose_name='会议',max_length=10, default=0)
    group_management = models.FloatField(verbose_name='班组管理',max_length=10, default=0)
    record = models.FloatField(verbose_name='记录',max_length=10, default=0)
    borrow_time = models.FloatField(verbose_name='外借时间',max_length=10, default=0)
    borrow_name = models.CharField(max_length=15, verbose_name='外借分类',default=' ',null=True, blank=True)
    comments = models.CharField(max_length=250,verbose_name='备注',default=' ',null=True, blank=True)
    date = models.DateField(auto_now=False,verbose_name='日期',default=date.today())
    groups = models.CharField(max_length=20,default='',verbose_name='班组')
    
    def __str__(self):
        return '%s %s ' % (self.user, self.date)
    class Meta:
        verbose_name = '辅助工时'
        verbose_name_plural = '辅助工时'

class CoefficientSupport(models.Model):
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
    borrow_time = models.FloatField(verbose_name='外借',max_length=10,null=True, default=0, blank=True)
    class Meta:
        verbose_name = '辅助工时系数'
        verbose_name_plural = '辅助工时系数'
    
class Borrow(models.Model):
    borrow = models.CharField(verbose_name='外借分类',max_length=10,null=True, default='', blank=True)
    def __str__(self):
        return '%s ' % (self.borrow)
    class Meta:
        verbose_name = '外借工时'
        verbose_name_plural = '外借'

class GroupOp(models.Model):
    group_name = models.CharField(verbose_name='组名', max_length=10)
    op_id = models.ForeignKey(Op, db_column='op_id',on_delete=models.CASCADE,verbose_name='工步')
    class Meta:
        verbose_name = '班组长-工步与组对应关系'
        verbose_name_plural = '班组长-工步与组对应关系'
    def __str__(self):
        return '%s %s' % (self.group_name,self.op_id)

class GroupPerform(models.Model):
    
    user = models.CharField(max_length=4, verbose_name='员工')
    natural_time = models.FloatField(max_length=4,verbose_name='工作时间',default=0)
    performance = models.FloatField(max_length=4,verbose_name='个人绩效',default=0)
    standard_time = models.FloatField(max_length=4,verbose_name='标准工时',default=0)
    real_time = models.FloatField(max_length=4,verbose_name='制造工时',default=0)
    supportive_time = models.FloatField(max_length=4,verbose_name='辅助工时',default=0)
    borrow_time = models.FloatField(max_length=4,verbose_name='外借工时',default=0)
    kpi = models.FloatField(max_length=4,verbose_name='工效比',default=0)
    efficiency = models.FloatField(max_length=4,verbose_name='工时有效率',default=0)
    date = models.DateField(auto_now=False)
    username = models.CharField(max_length=18,verbose_name='用户名',default=0)
    group = models.CharField(max_length=8,verbose_name='组',default='None')
    def __str__(self):
        return '%s %s %s %s %s %s %s %s %s %s %s %s' % (self.user, self.natural_time, self.performance, self.standard_time,self.real_time,
        self.supportive_time,self.borrow_time,self.kpi,self.efficiency,self.date,self.username,self.group)
    
    class Meta:
        verbose_name = '班组业绩统计'
        verbose_name_plural = '班组业绩统计'

class SfgComments(models.Model):
    sfg = models.CharField(max_length=5, verbose_name='SFG')
    comments = models.CharField(max_length=50, verbose_name='备注',null=True, default='', blank=True)
    class Meta:
        verbose_name = 'SFG备注信息'
        verbose_name_plural = 'SFG备注信息'
    

class OverTime(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default='',verbose_name='用户名')
    over_time = models.FloatField(verbose_name='加班', null=True, default=0, blank=True)
    over_time_type = models.CharField(max_length=3,verbose_name='加班种类', null=True, default=0, blank=True)
    is_paid = models.CharField(max_length=1,verbose_name='是否申请加班费', default=0)
    date = models.DateField(auto_now=False,default=date.today())
    groups = models.CharField(max_length=20,default='',verbose_name='班组')
    class Meta:
        verbose_name = '加班信息'
        verbose_name_plural = '加班信息'
    def __str__(self):
        return '%s %s %s %s %s %s' % (self.user.get_full_name(),self.over_time,self.over_time_type,self.is_paid,self.date,self.groups)

class TraceLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default='',verbose_name='用户名')
    username = models.CharField(max_length=4,verbose_name='用户', null=True, default='', blank=True)
    action_log =  models.CharField(max_length=30,verbose_name='动作', null=True, default='', blank=True)
    detail_message =  models.CharField(max_length=200,verbose_name='详情', null=True, default='', blank=True)
    comments = models.CharField(max_length=200,verbose_name='备注', null=True, default='', blank=True)    
    date = models.DateTimeField(auto_now=True)
    def __str__(self):
        return '%s %s %s %s %s' % (self.username,self.action_log,self.detail_message,self.comments,self.date)
    class Meta:
        verbose_name = 'Log'
        verbose_name_plural = 'Logs'

class AnnualLeave(models.Model):
    user = models.CharField(max_length=4,verbose_name='用户')
    leave_type = models.CharField(max_length=3,verbose_name='用户')
    start_date = models.DateTimeField(verbose_name='开始日期')
    end_date = models.DateTimeField(verbose_name='截止日期')
    hours = models.FloatField(verbose_name='时间', default=0)
    remarks = models.CharField(max_length=30,verbose_name='备注')
    class Meta:
        verbose_name = '休假'
        verbose_name_plural = '休假'


class WorkGroups(models.Model):
    group_name = models.CharField(max_length=20,verbose_name='所有工作组')
    def __str__(self):
        return '%s ' % (self.group_name)
    class Meta:
        verbose_name = '所有组'
        verbose_name_plural = '所有组'

class UserGroups(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default='',verbose_name='用户名')
    work_group = models.ForeignKey(WorkGroups, db_column='group_name',on_delete=models.CASCADE,verbose_name='工作组')
    def __str__(self):
        return '%s %s ' % (self.user,self.work_group)
    class Meta:
        verbose_name = '用户工作组'
        verbose_name_plural = '用户工作组'