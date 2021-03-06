from django.db import models
from django_google_maps import fields as map_fields
import datetime
from places.fields import PlacesField
from django.utils import timezone
from tempus_dominus.widgets import DatePicker, TimePicker, DateTimePicker
from django.utils import timezone
import re


class Event(models.Model):
    title = models.CharField(verbose_name="Event Name",max_length=200)
    pub_date = models.DateTimeField(auto_now_add=True)
    org_name = models.CharField(verbose_name="Organization Name",max_length=254, null=True, blank=True)
    description = models.CharField(verbose_name="Event Description", max_length=4096, null=True, blank=True)
    pic = models.CharField(verbose_name="Event Picture", max_length=1024, null=False, blank=False, default="https://avatars2.githubusercontent.com/u/3195011?s=460&u=f421eadccb78b212d516b6b38cab7f2de97522e4&v=4")
    date = models.DateTimeField()
    owner_id = models.IntegerField(null=False, default=1)
    address = PlacesField(verbose_name="Event Address", blank=True)
    money_goal = models.DecimalField(verbose_name="Donation Goal", max_digits=8, decimal_places=2, null=False, default=0)
    money_received = models.DecimalField(max_digits=8, decimal_places=2, null=False, default=0)
    hours_received = models.DecimalField(max_digits=8, decimal_places=2, null=False, default=0)

    def simple_address(self):
        return ", ".join(str(self.address).split(", ")[:-2])\

    def add_money(self, amount):
        print(amount)
        if amount > 0:
            if (self.money_received + amount >= 999999.99):
                self.money_received = 999999.99
            else:
                self.money_received+=amount

    def add_hours(self, amount):
        if amount > 0:
            if (self.hours_received + amount >= 999999.99):
                self.hours_received = 999999.99
            else:
                self.hours_received+=amount

    def money_remaining(self):
        return self.money_goal-self.money_received

    def met(self):
        return (self.money_goal <= self.money_received)
    met.boolean = True

    def surplus(self):
        return (self.money_goal < self.money_received)
    surplus.boolean = True

    def percentage(self):
        if (self.met()):
            return 100
        else:
            return int(self.money_received*100/self.money_goal)

    def remaining(self):
        if (self.met()):
            return 0
        else:
            return self.money_goal-self.money_received

    def ordered_pledges(self):
        return self.pledge_set.order_by('-date')

    def get_absolute_url(self):
        return "/events/%i/" % (self.pk)

    def __str__(self):
        return self.title

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'

class Pledge(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    payer_id = models.IntegerField(null=False, default=1)
    payment_text = models.CharField(max_length = 1024)
    payment_amount = models.DecimalField(max_digits=8, decimal_places=2, null=True)
    hours_amount = models.DecimalField(max_digits=8, decimal_places=2, null=True)
    date = models.DateTimeField(auto_now_add=True)
    confirmed = models.BooleanField(null=False, default=False)

    def confirm(self):
        self.confirmed = True
