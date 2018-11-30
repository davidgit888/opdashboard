# Generated by Django 2.1.1 on 2018-11-26 15:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0021_auto_20181126_1410'),
    ]

    operations = [
        migrations.AlterField(
            model_name='groupperform',
            name='performance',
            field=models.FloatField(default=0, max_length=4, verbose_name='个人绩效'),
        ),
        migrations.AlterField(
            model_name='groupperform',
            name='standard_time',
            field=models.FloatField(default=0, max_length=4, verbose_name='标准工时'),
        ),
        migrations.AlterField(
            model_name='groupperform',
            name='username',
            field=models.CharField(default=0, max_length=18, verbose_name='用户名'),
        ),
    ]
