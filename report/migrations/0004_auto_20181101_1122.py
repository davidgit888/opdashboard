# Generated by Django 2.1.1 on 2018-11-01 11:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0003_auto_20181101_0912'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='sfg_id',
            field=models.ForeignKey(db_column='sfg_id', on_delete=django.db.models.deletion.CASCADE, related_name='sfmprod_sfgid', to='report.SfmProd'),
        ),
        migrations.AlterField(
            model_name='report',
            name='type_name',
            field=models.ForeignKey(db_column='type_name', on_delete=django.db.models.deletion.CASCADE, related_name='std_typename', to='report.TypeStandard'),
        ),
        migrations.AlterField(
            model_name='typestandard',
            name='type_name',
            field=models.CharField(max_length=30),
        ),
    ]
