# Generated by Django 2.1.1 on 2018-11-07 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0005_auto_20181107_1441'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='sfg_id',
            field=models.CharField(default='', max_length=15, verbose_name='SFG'),
        ),
        migrations.AlterField(
            model_name='sfmprod',
            name='sfg_id',
            field=models.CharField(default='', max_length=15, verbose_name='SFG'),
        ),
    ]
