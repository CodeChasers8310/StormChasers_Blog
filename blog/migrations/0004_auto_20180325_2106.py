# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-03-26 02:06
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20180321_2006'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='user_id',
            new_name='user',
        ),
    ]