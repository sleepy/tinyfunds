# Generated by Django 3.1.1 on 2020-11-09 05:38

from django.db import migrations
import places.fields


class Migration(migrations.Migration):

    dependencies = [
        ('tinyfunds', '0012_auto_20201109_0527'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='location',
            field=places.fields.PlacesField(default='Charlottesville, 50, 50', max_length=255),
        ),
    ]
