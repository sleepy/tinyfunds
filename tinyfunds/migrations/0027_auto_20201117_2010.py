# Generated by Django 3.1.1 on 2020-11-17 20:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tinyfunds', '0026_remove_event_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='pledge',
            name='hours_amount',
            field=models.DecimalField(decimal_places=2, max_digits=8, null=True),
        ),
        migrations.AlterField(
            model_name='pledge',
            name='payment_amount',
            field=models.DecimalField(decimal_places=2, max_digits=8, null=True),
        ),
    ]
