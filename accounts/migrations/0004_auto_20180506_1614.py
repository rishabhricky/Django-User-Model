# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2018-05-06 16:14
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='username',
            field=models.CharField(max_length=255, unique=True, validators=[django.core.validators.RegexValidator(code='invalid_username', message='Username must be alphanumeric or contain any of the following:". @ + -"', regex='^[a-zA-Z0-9.+-]*$')]),
        ),
    ]
