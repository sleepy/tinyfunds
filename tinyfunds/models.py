from django.db import models
from django_google_maps import fields as map_fields
import datetime
from places.fields import PlacesField
from django.utils import timezone

class Event(models.Model):
    title = models.CharField(max_length=200)
    pub_date = models.DateTimeField(auto_now_add=True)
    org_name = models.CharField(max_length=254, null=True, blank=True)
    description = models.CharField(max_length=254, null=True, blank=True)
    pic = models.CharField(max_length=1024, null=False, blank=False, default="https://avatars2.githubusercontent.com/u/3195011?s=460&u=f421eadccb78b212d516b6b38cab7f2de97522e4&v=4")
    event_date = models.DateTimeField(auto_now_add=False, null=True)
    owner_id = models.IntegerField(null=False, default=1)
    address = PlacesField(blank=True)
    money_goal = models.DecimalField(max_digits=8, decimal_places=2, null=False, default=0)
    money_received = models.DecimalField(max_digits=8, decimal_places=2, null=False, default=0)

    def add_money(self, amount):
        self.money_received+=amount

    def money_remaining(self):
        return self.money_goal-self.money_received

    def surplus(self):
        return (self.money_goal < self.money_received)
    surplus.boolean = True

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
    payment_amount = models.DecimalField(max_digits=8, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
