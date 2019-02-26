# Generated by Django 2.1.1 on 2019-02-26 18:44

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0042_auto_20190109_1438'),
    ]

    operations = [
        migrations.AddField(
            model_name='groupperform',
            name='date_create',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='overtime',
            name='date',
            field=models.DateField(default=datetime.date(2019, 2, 26)),
        ),
        migrations.AlterField(
            model_name='report',
            name='date',
            field=models.DateField(default=datetime.date(2019, 2, 26)),
        ),
        migrations.AlterField(
            model_name='report',
            name='date_time',
            field=models.DateTimeField(auto_created=True, default=datetime.datetime(2019, 2, 26, 18, 44, 14, 936268), verbose_name='提交时间'),
        ),
        migrations.AlterField(
            model_name='supportivetime',
            name='date',
            field=models.DateField(default=datetime.date(2019, 2, 26), verbose_name='日期'),
        ),
    ]
