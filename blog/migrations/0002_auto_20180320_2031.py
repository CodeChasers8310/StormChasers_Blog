# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-03-21 01:31
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='image',
            old_name='blog_post_id',
            new_name='top_post_id',
        ),
    ]
