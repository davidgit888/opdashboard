# Generated by Django 2.1.1 on 2019-01-07 15:58

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0037_auto_20190107_1534'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='date_time',
            field=models.DateTimeField(auto_created=True, default=datetime.datetime(2019, 1, 7, 15, 58, 36, 926319), verbose_name='提交时间'),
        ),
    ]