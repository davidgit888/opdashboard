# Generated by Django 2.1.1 on 2018-11-22 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0017_auto_20181122_1203'),
    ]

    operations = [
        migrations.AlterField(
            model_name='supportivetime',
            name='borrow_name',
            field=models.CharField(blank=True, default='', max_length=15, null=True, verbose_name='外借分类'),
        ),
    ]