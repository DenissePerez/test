# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-04-26 15:31
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('helloworld', '0016_auto_20170425_1510'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='procesovisita',
            name='usuario',
        ),
        migrations.AlterField(
            model_name='solicitud',
            name='fecha_entrega',
            field=models.DateField(default=datetime.datetime(2017, 5, 14, 10, 31, 17, 166655)),
        ),
    ]
