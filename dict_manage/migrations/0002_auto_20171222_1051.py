# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-12-22 10:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dict_manage', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='created_at',
            field=models.DateTimeField(auto_now=True, verbose_name='created_at'),
        ),
        migrations.AlterField(
            model_name='category',
            name='updated_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='updated_at'),
        ),
    ]
