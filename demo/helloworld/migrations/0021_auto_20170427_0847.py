# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-04-27 13:47
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('helloworld', '0020_auto_20170427_0807'),
    ]

    operations = [
        migrations.RenameField(
            model_name='procesosolicitud',
            old_name='text',
            new_name='Título',
        ),
        migrations.AlterField(
            model_name='solicitud',
            name='fecha_respuesta',
            field=models.DateField(default=datetime.datetime(2017, 5, 15, 8, 47, 33, 94106)),
        ),
    ]
