# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-04-27 13:07
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('helloworld', '0019_auto_20170427_0754'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='solicitud',
            name='fecha_entrega',
        ),
        migrations.AddField(
            model_name='solicitud',
            name='fecha_respuesta',
            field=models.DateField(default=datetime.datetime(2017, 5, 15, 8, 7, 22, 654529)),
        ),
    ]
