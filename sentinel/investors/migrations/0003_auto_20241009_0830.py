# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2024-10-09 01:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('investors', '0002_auto_20210301_1619'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deposit',
            name='level',
            field=models.PositiveIntegerField(db_index=True, editable=False),
        ),
        migrations.AlterField(
            model_name='deposit',
            name='lft',
            field=models.PositiveIntegerField(db_index=True, editable=False),
        ),
        migrations.AlterField(
            model_name='deposit',
            name='rght',
            field=models.PositiveIntegerField(db_index=True, editable=False),
        ),
    ]
