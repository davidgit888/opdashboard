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

class TypeStandard(models.Model):
    type_name = models.CharField(max_length=30)
    op_id = models.IntegerField()
    op_name = models.CharField(max_length=10)
    class Meta:
        verbose_name = '标准工时'
        verbose_name_plural = '标准工时'

class Report(models.Model):
    sfg_id = models.ForeignKey(SfmProd, db_column='sfg_id', on_delete=models.CASCADE)
    type_name = models.ForeignKey(SfmProd, db_column='type_name', on_delete=models.CASCADE)
    op_id = models.IntegerField()
    prob = models.CharField(max_length=20)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    standard_tiem = models.FloatField(max_length=4)
    real_time = models.FloatField(max_length=4)
    date = models.DateField()
    class Meta:
        verbose_name = '报工平台'
        verbose_name_plural = '报工平台'

class OtherInfo(models.Model):
    sfg_id = models.ForeignKey(Report, db_column='sfg_id', on_delete=models.CASCADE)
    supportive_time = models.FloatField(max_length=4)
    borrow_time = models.FloatField(max_length=4)
    class Meta:
        verbose_name = '其他信息'
        verbose_name_plural = '其他信息'





