# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-04-25 17:43
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('helloworld', '0007_auto_20170425_1242'),
    ]

    operations = [
        migrations.AlterField(
            model_name='acta',
            name='acta',
            field=models.FileField(blank=True, null=True, upload_to='uploads/'),
        ),
        migrations.AlterField(
            model_name='solicitud',
            name='fecha_entrega',
            field=models.DateField(default=datetime.datetime(2017, 5, 13, 12, 43, 6, 492641)),
        ),
    ]