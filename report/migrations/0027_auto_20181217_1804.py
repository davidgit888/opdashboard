# Generated by Django 2.1.1 on 2018-12-17 18:04

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0026_auto_20181214_0855'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='date_time',
            field=models.DateTimeField(auto_created=True, default=datetime.datetime(2018, 12, 17, 18, 4, 9, 915554)),
        ),
        migrations.AlterField(
            model_name='overtime',
            name='date',
            field=models.DateField(default=datetime.date(2018, 12, 17)),
        ),
        migrations.AlterField(
            model_name='report',
            name='date',
            field=models.DateField(default=datetime.date(2018, 12, 17)),
        ),
        migrations.AlterField(
            model_name='supportivetime',
            name='date',
            field=models.DateField(default=datetime.date(2018, 12, 17), verbose_name='日期'),
        ),
    ]