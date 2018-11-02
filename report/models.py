from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class SfmProd(models.Model):
    sfg_id = models.IntegerField()
    type_name = models.CharField(max_length=30)
    class Meta:
        verbose_name = 'SFM信息'
        verbose_name_plural = 'SFM信息'
    def __str__(self):
    
        return '%s %s' % (self.sfg_id, self.type_name)

class Prob(models.Model):
    prob_info = models.CharField(max_length=20)
    class Meta:
        verbose_name = "测头信息"
        verbose_name_plural = "测头信息"
    def __str__(self):
        
        return '%s' % (self.prob_info)
class TypeStandard(models.Model):
    type_name = models.CharField(max_length=30)
    op_id = models.IntegerField()
    prob_info = models.ForeignKey(Prob, verbose_name='测针信息',db_column='prob_info',on_delete=models.CASCADE,null=True, blank=True)
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
    sfg_id = models.ForeignKey(SfmProd, db_column='sfg_id', related_name='sfmprod_sfgid',on_delete=models.CASCADE)
    type_name = models.CharField(max_length=20,default='')
    op_id = models.ForeignKey(Op, db_column='op_id',on_delete=models.CASCADE)
    prob = models.CharField(max_length=20,default='')
    qty = models.FloatField(max_length=4, default=1)
    #user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    user = models.CharField(max_length=4,default='')
    standard_tiem = models.FloatField(max_length=4)
    real_time = models.FloatField(max_length=4)
    date = models.DateField(auto_now=True)
    def __str__(self):
        return '%s ' % (self.date)
    class Meta:
        verbose_name = '报工平台'
        verbose_name_plural = '报工平台'

class OtherInfo(models.Model):
    sfg_id = models.ForeignKey(Report, db_column='sfg_id', on_delete=models.CASCADE)
    supportive_time = models.FloatField(max_length=4)
    borrow_time = models.FloatField(max_length=4)
    date = models.DateField(auto_now=True)
    def __str__(self):
        return '%s ' % (self.date)
    class Meta:
        verbose_name = '辅助工时'
        verbose_name_plural = '辅助工时'





