# Generated by Django 2.1.1 on 2018-11-02 14:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0013_auto_20181102_1402'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='otherinfo',
            options={'verbose_name': '辅助工时', 'verbose_name_plural': '辅助工时'},
        ),
        migrations.AlterField(
            model_name='report',
            name='prob',
            field=models.CharField(default='', max_length=20),
        ),
        migrations.AlterField(
            model_name='report',
            name='type_name',
            field=models.CharField(default='', max_length=20),
        ),
        migrations.AlterField(
            model_name='report',
            name='user',
            field=models.CharField(default='', max_length=4),
        ),
        migrations.AlterField(
            model_name='typestandard',
            name='prob_info',
            field=models.ForeignKey(blank=True, db_column='prob_info', null=True, on_delete=django.db.models.deletion.CASCADE, to='report.Prob', verbose_name='测针信息'),
        ),
        migrations.AlterField(
            model_name='typestandard',
            name='standard_time',
            field=models.CharField(max_length=10, verbose_name='标准工时'),
        ),
    ]
