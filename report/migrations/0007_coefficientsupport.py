# Generated by Django 2.1.1 on 2018-11-07 19:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0006_auto_20181107_1443'),
    ]

    operations = [
        migrations.CreateModel(
            name='CoefficientSupport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rest', models.FloatField(blank=True, default=0, max_length=10, null=True, verbose_name='休息')),
                ('clean_time', models.FloatField(blank=True, default=0, max_length=10, null=True, verbose_name='卫生')),
                ('inside_group', models.FloatField(blank=True, default=0, max_length=10, null=True, verbose_name='组内')),
                ('outside_group', models.FloatField(blank=True, default=0, max_length=10, null=True, verbose_name='组外')),
                ('complete_machine', models.FloatField(blank=True, default=0, max_length=10, null=True, verbose_name='整机')),
                ('granite', models.FloatField(blank=True, default=0, max_length=10, null=True, verbose_name='花岗石')),
                ('prob', models.FloatField(blank=True, default=0, max_length=10, null=True, verbose_name='测头')),
                ('shortage', models.FloatField(blank=True, default=0, max_length=10, null=True, verbose_name='补缺件')),
                ('plan_change', models.FloatField(blank=True, default=0, max_length=10, null=True, verbose_name='计划调整')),
                ('human_quality_issue_rework', models.FloatField(blank=True, default=0, max_length=10, null=True, verbose_name='人为质量问题返工')),
                ('item_quality_issue', models.FloatField(blank=True, default=0, max_length=10, null=True, verbose_name='零件质量问题')),
                ('human_quality_issue_repair', models.FloatField(blank=True, default=0, max_length=10, null=True, verbose_name='人为质量问题返修')),
                ('equipment_mantainence', models.FloatField(blank=True, default=0, max_length=10, null=True, verbose_name='设备维护')),
                ('inventory_check', models.FloatField(blank=True, default=0, max_length=10, null=True, verbose_name='库存核查')),
                ('quality_check', models.FloatField(blank=True, default=0, max_length=10, null=True, verbose_name='质量审核')),
                ('document', models.FloatField(blank=True, default=0, max_length=10, null=True, verbose_name='档案整理')),
                ('conference', models.FloatField(blank=True, default=0, max_length=10, null=True, verbose_name='会议')),
                ('group_management', models.FloatField(blank=True, default=0, max_length=10, null=True, verbose_name='班组管理')),
                ('record', models.FloatField(blank=True, default=0, max_length=10, null=True, verbose_name='记录')),
            ],
        ),
    ]
