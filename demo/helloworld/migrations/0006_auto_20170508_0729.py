# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-05-08 12:29
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('helloworld', '0005_auto_20170508_0727'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solicitud',
            name='fecha_respuesta',
            field=models.DateField(default=datetime.datetime(2017, 5, 26, 7, 29, 14, 868236)),
        ),
    ]
