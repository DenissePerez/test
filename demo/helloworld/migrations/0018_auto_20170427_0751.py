# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-04-27 12:51
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('helloworld', '0017_auto_20170426_1031'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solicitud',
            name='fecha_entrega',
            field=models.DateField(default=datetime.datetime(2017, 5, 15, 7, 51, 25, 879849)),
        ),
    ]