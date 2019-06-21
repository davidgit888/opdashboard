# Generated by Django 2.1.1 on 2019-06-05 18:08

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('report', '0047_auto_20190326_1043'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='material',
            options={'verbose_name': '物耗材料', 'verbose_name_plural': '物耗材料'},
        ),
        migrations.AlterModelOptions(
            name='materialapprove',
            options={'verbose_name': '物耗申请审批', 'verbose_name_plural': '物耗申请审批'},
        ),
        migrations.AlterModelOptions(
            name='materialget',
            options={'verbose_name': '物耗材料到货', 'verbose_name_plural': '物耗材料到货'},
        ),
        migrations.AlterModelOptions(
            name='meterialsurplus',
            options={'verbose_name': '物耗结余', 'verbose_name_plural': '物耗结余'},
        ),
        migrations.AlterModelOptions(
            name='meterialuse',
            options={'verbose_name': '物耗领用', 'verbose_name_plural': '物耗领用'},
        ),
        migrations.AlterField(
            model_name='materialapprove',
            name='qty',
            field=models.IntegerField(default=0, verbose_name='审批数量'),
        ),
        migrations.AlterField(
            model_name='materialapprove',
            name='qty_request',
            field=models.IntegerField(default=0, verbose_name='申请数量'),
        ),
        migrations.AlterField(
            model_name='overtime',
            name='date',
            field=models.DateField(default=datetime.date(2019, 6, 5)),
        ),
        migrations.AlterField(
            model_name='report',
            name='date',
            field=models.DateField(default=datetime.date(2019, 6, 5)),
        ),
        migrations.AlterField(
            model_name='report',
            name='date_time',
            field=models.DateTimeField(auto_created=True, default=datetime.datetime(2019, 6, 5, 18, 8, 49, 945101), verbose_name='提交时间'),
        ),
        migrations.AlterField(
            model_name='supportivetime',
            name='date',
            field=models.DateField(default=datetime.date(2019, 6, 5), verbose_name='日期'),
        ),
    ]