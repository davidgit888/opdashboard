# Generated by Django 2.1.1 on 2020-01-06 12:00

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0052_auto_20191128_1821'),
    ]

    operations = [
        migrations.AddField(
            model_name='annualleave',
            name='staff_no',
            field=models.CharField(default=0, max_length=10, verbose_name='工号'),
        ),
    
    ]