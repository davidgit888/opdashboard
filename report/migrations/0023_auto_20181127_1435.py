# Generated by Django 2.1.1 on 2018-11-27 14:35

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0022_auto_20181126_1538'),
    ]

    operations = [
        migrations.CreateModel(
            name='SfgComments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sfg', models.CharField(max_length=5, verbose_name='SFG')),
                ('comments', models.CharField(blank=True, default='', max_length=50, null=True, verbose_name='备注')),
            ],
        ),
        migrations.AlterField(
            model_name='report',
            name='date',
            field=models.DateField(default=datetime.date(2018, 11, 27)),
        ),
        migrations.AlterField(
            model_name='supportivetime',
            name='date',
            field=models.DateField(default=datetime.date(2018, 11, 27), verbose_name='日期'),
        ),
    ]
