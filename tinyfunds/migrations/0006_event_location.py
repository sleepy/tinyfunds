# Generated by Django 3.1.1 on 2020-11-03 17:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tinyfunds', '0005_event_owner_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='location',
            field=models.CharField(blank=True, max_length=254, null=True),
        ),
    ]
