# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-08-24 10:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_auto_20190824_1608'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='time',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
