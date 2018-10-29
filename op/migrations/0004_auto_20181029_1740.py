# Generated by Django 2.1.1 on 2018-10-29 17:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('op', '0003_auto_20181029_1735'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deliveredcmm',
            name='Apr',
            field=models.IntegerField(blank=True, max_length=5, null=True),
        ),
        migrations.AlterField(
            model_name='deliveredcmm',
            name='Aug',
            field=models.IntegerField(blank=True, max_length=5, null=True),
        ),
        migrations.AlterField(
            model_name='deliveredcmm',
            name='Dec',
            field=models.IntegerField(blank=True, max_length=5, null=True),
        ),
        migrations.AlterField(
            model_name='deliveredcmm',
            name='Feb',
            field=models.IntegerField(blank=True, max_length=5, null=True),
        ),
        migrations.AlterField(
            model_name='deliveredcmm',
            name='Jan',
            field=models.IntegerField(blank=True, max_length=5, null=True),
        ),
        migrations.AlterField(
            model_name='deliveredcmm',
            name='Jul',
            field=models.IntegerField(blank=True, max_length=5, null=True),
        ),
        migrations.AlterField(
            model_name='deliveredcmm',
            name='Jun',
            field=models.IntegerField(blank=True, max_length=5, null=True),
        ),
        migrations.AlterField(
            model_name='deliveredcmm',
            name='Mar',
            field=models.IntegerField(blank=True, max_length=5, null=True),
        ),
        migrations.AlterField(
            model_name='deliveredcmm',
            name='May',
            field=models.IntegerField(blank=True, max_length=5, null=True),
        ),
        migrations.AlterField(
            model_name='deliveredcmm',
            name='Nov',
            field=models.IntegerField(blank=True, max_length=5, null=True),
        ),
        migrations.AlterField(
            model_name='deliveredcmm',
            name='Oct',
            field=models.IntegerField(blank=True, max_length=5, null=True),
        ),
        migrations.AlterField(
            model_name='deliveredcmm',
            name='Sep',
            field=models.IntegerField(blank=True, max_length=5, null=True),
        ),
        migrations.AlterField(
            model_name='neworder',
            name='Apr',
            field=models.IntegerField(blank=True, max_length=5, null=True),
        ),
        migrations.AlterField(
            model_name='neworder',
            name='Aug',
            field=models.IntegerField(blank=True, max_length=5, null=True),
        ),
        migrations.AlterField(
            model_name='neworder',
            name='Dec',
            field=models.IntegerField(blank=True, max_length=5, null=True),
        ),
        migrations.AlterField(
            model_name='neworder',
            name='Feb',
            field=models.IntegerField(blank=True, max_length=5, null=True),
        ),
        migrations.AlterField(
            model_name='neworder',
            name='Jan',
            field=models.IntegerField(blank=True, max_length=5, null=True),
        ),
        migrations.AlterField(
            model_name='neworder',
            name='Jul',
            field=models.IntegerField(blank=True, max_length=5, null=True),
        ),
        migrations.AlterField(
            model_name='neworder',
            name='Jun',
            field=models.IntegerField(blank=True, max_length=5, null=True),
        ),
        migrations.AlterField(
            model_name='neworder',
            name='Mar',
            field=models.IntegerField(blank=True, max_length=5, null=True),
        ),
        migrations.AlterField(
            model_name='neworder',
            name='May',
            field=models.IntegerField(blank=True, max_length=5, null=True),
        ),
        migrations.AlterField(
            model_name='neworder',
            name='Nov',
            field=models.IntegerField(blank=True, max_length=5, null=True),
        ),
        migrations.AlterField(
            model_name='neworder',
            name='Oct',
            field=models.IntegerField(blank=True, max_length=5, null=True),
        ),
        migrations.AlterField(
            model_name='neworder',
            name='Sep',
            field=models.IntegerField(blank=True, max_length=5, null=True),
        ),
        migrations.AlterField(
            model_name='waitingorderandinventory',
            name='AuctalAssemblyQty',
            field=models.IntegerField(blank=True, max_length=5, null=True),
        ),
        migrations.AlterField(
            model_name='waitingorderandinventory',
            name='BackLogTendency',
            field=models.IntegerField(blank=True, max_length=5, null=True),
        ),
        migrations.AlterField(
            model_name='waitingorderandinventory',
            name='Backlog',
            field=models.IntegerField(blank=True, max_length=5, null=True),
        ),
        migrations.AlterField(
            model_name='waitingorderandinventory',
            name='NetAvailable',
            field=models.IntegerField(blank=True, max_length=5, null=True),
        ),
        migrations.AlterField(
            model_name='waitingorderandinventory',
            name='NetAvailableTendency',
            field=models.IntegerField(blank=True, max_length=5, null=True),
        ),
        migrations.AlterField(
            model_name='waitingorderandinventory',
            name='OrderQty',
            field=models.IntegerField(blank=True, max_length=5, null=True),
        ),
        migrations.AlterField(
            model_name='waitingorderandinventory',
            name='ShipmentQty',
            field=models.IntegerField(blank=True, max_length=5, null=True),
        ),
        migrations.AlterField(
            model_name='waitingorderandinventory',
            name='ToBeExcutedOrder',
            field=models.IntegerField(blank=True, max_length=5, null=True),
        ),
        migrations.AlterField(
            model_name='waitingorderandinventory',
            name='ToBeExcutedTendency',
            field=models.IntegerField(blank=True, max_length=5, null=True),
        ),
    ]
