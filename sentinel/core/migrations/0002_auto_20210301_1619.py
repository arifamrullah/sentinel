# Generated by Django 3.1.7 on 2021-03-01 09:19

import django.core.validators
from django.db import migrations, models
import re


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='office',
            name='phone',
            field=models.CharField(blank=True, max_length=30, null=True, validators=[django.core.validators.RegexValidator(re.compile('^\\d+(?:\\-\\d+)*\\Z'), code='invalid', message='Enter only digits number')], verbose_name='phone no.'),
        ),
        migrations.AlterField(
            model_name='office',
            name='postal_code',
            field=models.CharField(default='', max_length=10, validators=[django.core.validators.RegexValidator(re.compile('^\\d+(?:,\\d+)*\\Z'), code='invalid', message='Enter only digits number')], verbose_name='postal code'),
        ),
    ]
