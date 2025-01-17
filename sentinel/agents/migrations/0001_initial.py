# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-06-21 11:21
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields
import re


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('utils', '0001_initial'),
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Agent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('full_name', models.CharField(max_length=100, verbose_name='full name')),
                ('national_id_card_no', models.CharField(max_length=30, null=True, validators=[django.core.validators.RegexValidator(re.compile('^\\d+(?:\\,\\d+)*\\Z'), code=b'invalid', message=b'Enter only digits number'), django.core.validators.MaxLengthValidator(16), django.core.validators.MinLengthValidator(16)], verbose_name='national id card no')),
                ('place_of_birth', models.CharField(max_length=50, verbose_name='place of birth')),
                ('date_of_birth', models.DateField(verbose_name='date of birth')),
                ('gender', models.CharField(choices=[(b'M', 'Male'), (b'F', 'Female')], default=b'M', max_length=5, verbose_name='gender')),
                ('phone', models.CharField(blank=True, max_length=30, validators=[django.core.validators.RegexValidator(re.compile('^\\d+(?:\\-\\d+)*\\Z'), code=b'invalid', message=b'Enter only digits number')], verbose_name='phone no.')),
                ('mobile1', models.CharField(max_length=30, validators=[django.core.validators.RegexValidator(re.compile('^\\d+(?:\\-\\d+)*\\Z'), code=b'invalid', message=b'Enter only digits number')], verbose_name='primary mobile no.')),
                ('mobile2', models.CharField(blank=True, max_length=30, null=True, validators=[django.core.validators.RegexValidator(re.compile('^\\d+(?:\\-\\d+)*\\Z'), code=b'invalid', message=b'Enter only digits number')], verbose_name='secondary mobile no.')),
                ('address', models.TextField(verbose_name='address')),
                ('postal_code', models.CharField(default=b'', max_length=10, validators=[django.core.validators.RegexValidator(re.compile('^\\d+(?:\\,\\d+)*\\Z'), code=b'invalid', message=b'Enter only digits number')], verbose_name='postal code')),
                ('email', models.EmailField(max_length=254, verbose_name='email')),
                ('bank_acc_name', models.CharField(max_length=50, verbose_name='bank account name')),
                ('bank_name', models.CharField(max_length=50, verbose_name='bank name')),
                ('bank_branch', models.CharField(max_length=50, verbose_name='bank branch')),
                ('bank_acc_no', models.CharField(max_length=30, validators=[django.core.validators.RegexValidator(re.compile('^\\d+(?:\\-\\d+)*\\Z'), code=b'invalid', message=b'Enter only digits number')], verbose_name='bank account no.')),
                ('tax_id_no', models.CharField(blank=True, max_length=30, verbose_name='tax id no.')),
                ('position', models.CharField(choices=[(b'finconsultant', 'Financial Consultant'), (b'manager', 'Manager'), (b'director', 'Director')], default=b'finconsultant', max_length=50, verbose_name='position')),
                ('code', models.CharField(max_length=30, unique=True, verbose_name='agents code')),
                ('created_place', models.CharField(blank=True, max_length=50, null=True)),
                ('created_user', models.CharField(blank=True, max_length=30, null=True)),
                ('photo', models.ImageField(default=b'', upload_to=b'agents/photos/', verbose_name='photo')),
                ('agency_director', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='agencydirector', to='agents.Agent')),
                ('city', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='utils.City')),
                ('direct_leader', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='directleader', to='agents.Agent')),
                ('office_location', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.Office')),
                ('province', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='utils.Province')),
                ('recruiter', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='agentrecruiter', to='agents.Agent')),
                ('sad_or_rm', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sadrms', to='agents.Agent')),
            ],
            options={
                'ordering': ('-created',),
            },
        ),
    ]
