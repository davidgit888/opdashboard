# Generated by Django 2.1.1 on 2018-11-02 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0016_auto_20181102_1519'),
    ]

    operations = [
        migrations.AddField(
            model_name='otherinfo',
            name='date',
            field=models.DateField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='report',
            name='date',
            field=models.DateField(auto_now=True),
        ),
    ]
