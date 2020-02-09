from django.db import models
from django.contrib.auth.models import User, Group
from report.models import Op, WorkGroups
import datetime
# Create your models here.

class ManHours(models.Model):
    """
    Manufacture Hours
    """
    contract = models.CharField(max_length=30,verbose_name='合同号', default='',)
    sfg = models.CharField(max_length=15, verbose_name='SFG',default='')
    product_type = models.CharField(max_length=50,default='',verbose_name='机型')
    op = models.ForeignKey(Op, db_column='op_id',on_delete=models.CASCADE,verbose_name='工步')
    prob = models.CharField(max_length=20,default='',verbose_name='测头',null=True, blank=True)
    qty = models.FloatField(max_length=4, default='',verbose_name='数量')
    username = models.ForeignKey(User, on_delete=models.CASCADE, default='',verbose_name='用户名')
    standard = models.FloatField(max_length=4,verbose_name='标准价值工时',default=0)
    real_time = models.FloatField(verbose_name='实际工时',max_length=4,default=0)
    confirmed = models.FloatField(max_length=4,verbose_name='确认价值工时',default=0, blank = True)
    quote = models.FloatField(max_length=4,verbose_name='报价',default=0)
    cost_rate = models.FloatField(max_length=4,verbose_name='费率',default=0)
    date = models.DateField(auto_now=False)
    create_date = models.DateTimeField(auto_now=True, auto_created=True,verbose_name='创建时间')
    original_group = models.CharField(max_length=20,default='',verbose_name='原班组')
    work_group = models.CharField(max_length=20,default='',verbose_name='工作组')
    last_fix_date = models.DateTimeField(auto_now=True, auto_created=True,verbose_name='最后修改时间')
    last_fix_user = models.CharField(max_length=5,default='',verbose_name='最后修改人')
    last_fix_status = models.CharField(max_length=1000, default='',verbose_name='最后修改状态')
    is_active = models.BooleanField(default = False)
    flexible = models.TextField(null = True, blank = True, verbose_name='浮动列',default='')
    old_perform = models.IntegerField(verbose_name='业绩', default=0)

    def __str__(self):
        return '%s %s %s %s %s %s' %(self.contract, self.sfg, self.product_type,self.username,self.confirmed,self.date)

    class Meta:
        verbose_name = '制造工时统计'
        verbose_name_plural = '制造工时统计'


class Assistance(models.Model):
    contract = models.CharField(max_length=30,verbose_name='合同号', default='',)
    a_type = models.CharField(max_length=100,default='',verbose_name='类别', blank = True)
    a_category = models.CharField(max_length=100,default='',verbose_name='大类', blank = True)
    a_subject = models.CharField(max_length=100,default='',verbose_name='科目', blank = True)
    real_time = models.FloatField(verbose_name='实际工时',max_length=4,default=0,)
    quote = models.FloatField(max_length=4,verbose_name='报价',default=0)
    cost_rate = models.FloatField(max_length=4,verbose_name='费率',default=0)
    standard = models.FloatField(max_length=4,verbose_name='标准价值工时',default=0)
    confirmed = models.FloatField(max_length=4,verbose_name='确认价值工时',default=0)
    attach = models.CharField(max_length=200,verbose_name='附件', default='', blank = True)
    b_category = models.CharField(max_length=100,default='',verbose_name='外借科目大类', blank = True)
    b_subject = models.CharField(max_length=100,default='',verbose_name='外借科目小类', blank = True)
    expense = models.FloatField(max_length=10,verbose_name='期间费用',default=0, blank = True)
    original_group = models.CharField(max_length=20,default='',verbose_name='原班组')
    work_group = models.CharField(max_length=20,default='',verbose_name='工作组')
    username = models.ForeignKey(User, on_delete=models.CASCADE, default='',verbose_name='用户名')
    comments = models.TextField(null = True, blank = True,default='',verbose_name='备注')
    date = models.DateField(auto_now=False)
    create_date = models.DateTimeField(auto_now=True,auto_created=True,verbose_name='创建时间')
    last_fix_date = models.DateTimeField(auto_now=True, auto_created=True,verbose_name='最后修改时间')
    last_fix_user = models.CharField(max_length=5,default='',verbose_name='最后修改人')
    last_fix_status = models.CharField(max_length=1000, default='',verbose_name='最后修改状态')
    is_active = models.BooleanField(default = False)
    flexible = models.TextField(null = True, blank = True, verbose_name='浮动列',default='')
    old_perform = models.IntegerField(verbose_name='业绩', default=0)
    def __str__(self):
        return '%s %s %s %s %s %s' %(self.contract, self.a_type, self.a_subject,self.real_time,self.quote,self.cost_rate)
    class Meta:
        verbose_name = '非制造工时统计'
        verbose_name_plural = '非制造工时统计'

class AssisType(models.Model):
    a_type = models.CharField(max_length=100,default='',verbose_name='类别')
    a_category = models.CharField(max_length=100,default='',verbose_name='大类',blank = True)
    a_subject = models.CharField(max_length=100,default='',verbose_name='小类')
    b_category = models.CharField(max_length=100,default='',verbose_name='外借科目大类',blank = True,help_text="不用填写")
    b_subject = models.CharField(max_length=100,default='',verbose_name='外借科目小类',blank = True,help_text="不用填写")
    b_old_category = models.CharField(max_length=100,default='',verbose_name='对应老辅助工时或者外借工时',help_text="必须填写")
    create_date = models.DateTimeField(auto_now=True, auto_created=True,verbose_name='创建时间')
    last_fix_date = models.DateTimeField(auto_now=True, auto_created=True,verbose_name='最后修改时间')
    create_user = models.ForeignKey(User, on_delete=models.CASCADE, default='',verbose_name='创建人')
    last_fix_user = models.CharField(max_length=5,default='',verbose_name='最后修改人')
    last_fix_status = models.CharField(max_length=200, default='',verbose_name='最后修改状态')
    is_active = models.BooleanField(default = False,verbose_name='是否生效',help_text="必须填写")
    flexible = models.TextField(null = True, blank = True, verbose_name='保留列',default='')
    def __str__(self):
        return '%s %s %s %s %s %s' %(self.a_type, self.a_category, self.a_subject,self.b_category,self.b_subject,self.b_old_category)
    class Meta:
        verbose_name = '非制造工时种类'
        verbose_name_plural = '非制造工时种类'


class UserInfomation(models.Model):
    """UserInfo"""
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, default='',verbose_name='用户名', unique=True)
    staff_no = models.CharField(max_length=10,verbose_name='工号',default='')
    duty = models.CharField(max_length=10,verbose_name='职位',default='')
    email = models.CharField(max_length=50,verbose_name='邮箱',default='',blank=True)
    work_group = models.ForeignKey(WorkGroups, db_column='group_name',on_delete=models.CASCADE,verbose_name='工作组',default='')
    original_group = models.CharField(max_length=30,verbose_name='原班组',default='')
    mobile = models.IntegerField(verbose_name='电话',blank=True)
    cost_rate = models.FloatField(max_length=4,verbose_name='费率',default=0)
    quote = models.FloatField(max_length=4,verbose_name='报价',default=0)
    flexible = models.TextField(null = True, blank = True, verbose_name='浮动列',default='')
    is_active = models.BooleanField(default = False,verbose_name='是否生效')
    permissions = models.ManyToManyField(to="Permissions", blank=True, verbose_name="个人权限")
    hiredate = models.DateField(auto_now=False, default=datetime.date.today(), verbose_name='入职时间')
    def __str__(self):
        return '%s %s %s %s %s %s' %(self.user_id, self.staff_no, self.duty,self.email,self.work_group,self.original_group)
    class Meta:
        verbose_name = '用户信息表'
        verbose_name_plural = '用户信息表'


class BorrowType(models.Model):
    """ 外借工时种类 """
    b_category = models.CharField(max_length=100,default='',verbose_name='外借种类',help_text="必须填写")
    b_subject = models.CharField(max_length=100,default='',verbose_name='外借小类',blank=True,help_text="必须填写")
    flexible = models.TextField(null = True, blank = True, verbose_name='保留列',default='')
    def __str__(self):
        return '%s %s %s' %(self.b_category, self.b_subject, self.flexible)
    class Meta:
        verbose_name = '外借工时分类'
        verbose_name_plural = '外借工时分类'

class Permissions(models.Model):
    title = models.CharField(max_length=300, default='',verbose_name='一级菜单')
    subtitle = models.CharField(max_length=300, default='', verbose_name='二级菜单')
    subtitle2 = models.CharField(max_length=300, default='', verbose_name='三级菜单',blank=True)
    url = models.CharField(max_length=200, default='', verbose_name='URL')
    flexible = models.TextField(null = True, blank = True, verbose_name='浮动列',default='')
    def __str__(self):
        return '%s %s %s %s' %(self.title, self.subtitle, self.subtitle2, self.url)
    class Meta:
        verbose_name = '所有权限'
        verbose_name_plural = '所有权限'

class GroupPermissions(models.Model):
    """All permissions list """
    group = models.ForeignKey(Group, on_delete=models.CASCADE, default='',verbose_name='组')
    permissions = models.ManyToManyField(to="Permissions", blank=True, verbose_name="组权限")
    def __str__(self):
        return '%s %s ' %(self.group, self.permissions)
    class Meta:
        verbose_name = '组权限'
        verbose_name_plural = '组权限'

# class UserPermissions(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, default='',verbose_name='用户')
#     permissions = models.ForeignKey(Permissions, on_delete=models.CASCADE, default='',verbose_name='权限')
#     def __str__(self):
#         return '%s %s ' %(self.group, self.permissions)
#     class Meta:
#         verbose_name = '用户权限'
#         verbose_name_plural = '用户权限'
class AgeParameters(models.Model):
    """Parameters for work age"""
    age = models.FloatField(max_length=4,verbose_name='工龄',default=0)
    para = models.FloatField(max_length=4,verbose_name='系数',default=0)


    def __str__(self):
        return '%s %s ' %(self.age, self.para)
    class Meta:
        verbose_name = '工龄系数'
        verbose_name_plural = '工龄系数'

class ProductParameters(models.Model):
    """Parameters for product"""
    product = models.CharField(max_length=50,verbose_name='产品线',default='')
    para = models.FloatField(max_length=4,verbose_name='系数',default=0)

    def __str__(self):
        return '%s %s ' %(self.product, self.para)
    class Meta:
        verbose_name = '产品线系数'
        verbose_name_plural = '产品线系数'

class AssemblyParameters(models.Model):
    """Parameters for 11 小部件"""
    attribute = models.CharField(max_length=50, verbose_name='属性', default='')
    para = models.FloatField(max_length=4, verbose_name='系数', default=1)
    def __str__(self):
        return '%s %s ' %(self.attribute, self.para)
    class Meta:
        verbose_name = '小部件系数'
        verbose_name_plural = '小部件系数'
