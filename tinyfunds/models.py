from django.db import models
import datetime
from django.utils import timezone

class Event(models.Model):
    idnum = models.PositiveIntegerField(primary_key=True)
    title = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    org_name = models.CharField(max_length=254, null=True, blank=True)
    description = models.CharField(max_length=254, null=True, blank=True)
    pic = models.CharField(max_length=1024, null=False, blank=False, default="https://avatars2.githubusercontent.com/u/3195011?s=460&u=f421eadccb78b212d516b6b38cab7f2de97522e4&v=4")
    event_date = models.DateTimeField(auto_now_add=True)

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

