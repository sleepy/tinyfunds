# Generated by Django 3.1.1 on 2020-11-09 04:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tinyfunds', '0009_merge_20201109_0443'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='location',
        ),
    ]
