# Generated by Django 2.1.1 on 2020-01-14 10:46

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jzgs', '0003_auto_20200107_0935'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfomation',
            name='hiredate',
            field=models.DateField(default=datetime.date(2020, 1, 14), verbose_name='入职时间'),
        ),
    ]
