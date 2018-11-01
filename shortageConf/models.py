from django.db import models

# Create your models here.

class Supplier(models.Model):
    supplier_name =  models.CharField(max_length=50,null=True, blank=True)
    quantity = models.IntegerField(null=True, blank=True)
    class Meta:
        verbose_name = '供应商'
        verbose_name_plural = '供应商'

class Overdue(models.Model):
    category = models.CharField(max_length=10,null=True, blank=True)
    quantity = models.IntegerField(null=True, blank=True)
    class Meta:
        verbose_name = '超期分类'
        verbose_name_plural = '超期分类'

class DeliveredTotal(models.Model):
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
        verbose_name = '发货缺件'
        verbose_name_plural = '发货缺件'

class ReasonAnalysis(models.Model):
    reason_category = models.CharField(max_length=15,null=True, blank=True)
    quantity = models.IntegerField(null=True, blank=True)
    class Meta:
        verbose_name = '原因分析'
        verbose_name_plural = '原因分析'
    