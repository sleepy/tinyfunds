# Generated by Django 3.1.1 on 2020-11-09 20:48

from django.db import migrations
import places.fields


class Migration(migrations.Migration):

    dependencies = [
        ('tinyfunds', '0019_merge_20201109_2048'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='address',
            field=places.fields.PlacesField(blank=True, max_length=255),
        ),
    ]
