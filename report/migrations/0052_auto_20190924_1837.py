# Generated by Django 2.1.1 on 2019-09-24 18:37

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0051_auto_20190924_1128'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='date_time',
            field=models.DateTimeField(auto_created=True, default=datetime.datetime(2019, 9, 24, 18, 37, 17, 874705), verbose_name='提交时间'),
        ),
        migrations.AlterField(
            model_name='supportivetime',
            name='date_create',
            field=models.DateTimeField(auto_created=True, default=datetime.datetime(2019, 9, 24, 18, 37, 17, 874705), verbose_name='创建时间'),
        ),
    ]
