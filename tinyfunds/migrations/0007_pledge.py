# Generated by Django 3.1.1 on 2020-11-09 02:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tinyfunds', '0006_event_address'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pledge',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payer_id', models.IntegerField(default=1)),
                ('payment_text', models.CharField(max_length=1024)),
                ('payment_amount', models.DecimalField(decimal_places=2, max_digits=8)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tinyfunds.event')),
            ],
        ),
    ]