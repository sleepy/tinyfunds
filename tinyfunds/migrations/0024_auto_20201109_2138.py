# Generated by Django 3.1.1 on 2020-11-09 21:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tinyfunds', '0023_event_address'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='event_date',
            new_name='date',
        ),
    ]
