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

    def __str__(self):
            
        return '%s %s %s %s' % (self.type_name, self.op_id, self.prob_info, self.standard_time)
    class Meta:
        verbose_name = '标准工时'
        verbose_name_plural = '标准工时'



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
    groups = models.CharField(max_length=20,default='',verbose_name='工作组组')
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
    vertical = models.FloatField(verbose_name='线性/垂直度修正',max_length=10,null=True, default=0, blank=True)
    date_create = models.DateTimeField(auto_created=True,verbose_name='创建时间',default=now())
    
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
    prob = models.FloatField(verbose_name='物流搬运',max_length=10,null=True, default=0, blank=True)
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
    vertical = models.FloatField(verbose_name='线性/垂直度修正',max_length=10,null=True, default=0, blank=True)
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
    group = models.CharField(max_length=10,verbose_name='原班组',default='None')
    work_group = models.CharField(max_length=10,verbose_name='工作组',default='')
    date_create = models.DateTimeField(auto_now=True)
    def __str__(self):
        return '%s %s %s %s %s %s %s %s %s %s %s %s %s' % (self.user, self.natural_time, self.performance, self.standard_time,self.real_time,
        self.supportive_time,self.borrow_time,self.kpi,self.efficiency,self.date,self.username,self.group,self.work_group)
    
    class Meta:
        verbose_name = '班组业绩统计'
        verbose_name_plural = '班组业绩统计'

class SfgComments(models.Model):
    sfg = models.CharField(max_length=20, verbose_name='SFG')
    comments = models.CharField(max_length=200, verbose_name='备注',null=True, default='', blank=True)
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

class DocType(models.Model):
    type = models.CharField(max_length=20,verbose_name='归档种类',unique=True)
    type_id = models.CharField(max_length=20,verbose_name='ID',default='',unique=True)
    def __str__(self):
        return '%s' %(self.type)

    class Meta:
        verbose_name = '归档种类'
        verbose_name_plural = '归档种类'
    
class DocInfo(models.Model):
    sfg = models.CharField(max_length=20,verbose_name='SFG')
    type = models.ForeignKey(DocType, db_column='type', on_delete=models.CASCADE, default='',verbose_name='归档种类')
    info = models.CharField(max_length=50, verbose_name='信息',default=0)
    date = models.DateTimeField(auto_now=True)
    def __str__(self):
        return '%s %s %s %s' %(self.sfg, self.type, self.info,self.date)
    class Meta:
        verbose_name = '归档信息'
        verbose_name_plural = '归档信息'

class Material(models.Model):
    sno = models.CharField(max_length=20,verbose_name='编号')
    name = models.CharField(max_length=50,verbose_name='物料名称')
    unit = models.CharField(max_length=10,verbose_name='单位')
    attribute = models.CharField(max_length=50,verbose_name='规格')
    comments = models.CharField(max_length=1,verbose_name='是否为包装材料')
    price = models.FloatField(max_length=10,verbose_name='单价',default='')
    def __str__(self):
        return '%s %s %s %s' %(self.sno, self.name, self.attribute,self.unit)
    class Meta:
        verbose_name = '物耗材料'
        verbose_name_plural = '物耗材料'    

class MaterialApprove(models.Model):
    sno = models.ForeignKey(Material, on_delete=models.CASCADE, default='',verbose_name='物料编号')
    year = models.IntegerField(verbose_name='年份')
    quarter = models.CharField(max_length=10,verbose_name='季度')
    group = models.ForeignKey(WorkGroups, on_delete=models.CASCADE, default='',verbose_name='班组')
    user = models.ForeignKey(User, on_delete=models.CASCADE, default='',verbose_name='用户名')
    qty = models.IntegerField(verbose_name='审批数量',default=0)
    qty_request = models.IntegerField(verbose_name='申请数量',default=0)
    qty_sup = models.FloatField(verbose_name='结余数量',default=0)
    qty_get = models.IntegerField(verbose_name='到货',default=0)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s %s %s %s %s %s' %(self.year, self.quarter, self.sno,self.group,self.qty,self.qty_request)
    class Meta:
        verbose_name = '物耗申请审批'
        verbose_name_plural = '物耗申请审批'

class MaterialGet(models.Model):
    sno = models.ForeignKey(Material, on_delete=models.CASCADE, default='',verbose_name='物料编号')
    year = models.IntegerField(verbose_name='年份')
    quarter = models.CharField(max_length=10,verbose_name='季度')
    group = models.ForeignKey(WorkGroups, on_delete=models.CASCADE, default='',verbose_name='班组')
    user = models.ForeignKey(User, on_delete=models.CASCADE, default='',verbose_name='用户名')
    qty = models.IntegerField( verbose_name='数量',default=0)
    date = models.DateTimeField(auto_now=True)
    def __str__(self):
        return '%s %s %s %s %s %s' %(self.year, self.quarter, self.sno,self.group,self.qty,self.date)
    class Meta:
        verbose_name = '物耗材料到货'
        verbose_name_plural = '物耗材料到货'

class MeterialUse(models.Model):
    sno = models.ForeignKey(Material, on_delete=models.CASCADE, default='',verbose_name='物料编号')
    year = models.IntegerField(max_length=4,verbose_name='年份')
    quarter = models.CharField(max_length=10,verbose_name='季度')
    group = models.ForeignKey(WorkGroups, on_delete=models.CASCADE, default='',verbose_name='班组')
    user = models.ForeignKey(User, on_delete=models.CASCADE, default='',verbose_name='用户名')
    qty = models.FloatField( verbose_name='数量',default=0)
    date = models.DateTimeField(auto_now=True)
    def __str__(self):
        return '%s %s %s %s %s %s' %(self.year, self.quarter, self.sno,self.group,self.qty,self.date)
    class Meta:
        verbose_name = '物耗领用'
        verbose_name_plural = '物耗领用'

class MeterialSurplus(models.Model):
    sno = models.ForeignKey(Material, on_delete=models.CASCADE, default='',verbose_name='物料编号')
    year = models.IntegerField(verbose_name='年份')
    quarter = models.CharField(max_length=10,verbose_name='季度')
    group = models.ForeignKey(WorkGroups, on_delete=models.CASCADE, default='',verbose_name='班组')
    qty = models.FloatField( verbose_name='数量',default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default='',verbose_name='用户名')
    date = models.DateTimeField(auto_now=True)
    def __str__(self):
        return '%s %s %s %s %s %s' %(self.year, self.quarter, self.sno,self.group,self.qty,self.date)
    class Meta:
        verbose_name = '物耗结余'
        verbose_name_plural = '物耗结余'


class UserInfo(models.Model):
    """UserInfo"""
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, default='',verbose_name='用户名')
    staff_no = models.CharField(max_length=10,verbose_name='工号',default='')
    duty = models.CharField(max_length=10,verbose_name='职位',default='')
    email = models.CharField(max_length=50,verbose_name='邮箱',default='')
    work_group = models.ForeignKey(WorkGroups, db_column='group_name',on_delete=models.CASCADE,verbose_name='工作组',default='')
    department = models.CharField(max_length=30,verbose_name='部门',default='')
    mobile = models.IntegerField(verbose_name='电话')


    def __str__(self):
        return '%s %s %s %s %s %s' %(self.user_id, self.staff_no, self.duty,self.email,self.work_group,self.department)
    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = '用户信息'
