from django import forms
from .models import Event
from datetime import datetime
from tempus_dominus.widgets import DatePicker, TimePicker, DateTimePicker
    
class CreateEventForm(forms.ModelForm):
    date = forms.DateTimeField(
        widget=DateTimePicker(
            options={
                'useCurrent': True,
                'collapse': False,
            },
            attrs={
                'append': 'fa fa-calendar',
                'icon_toggle': True,
            }
        ),
    )

    class Meta:
        model = Event
        fields = ['title', 'org_name', 'date', 'description', 'pic', 'address', 'money_goal', 'owner_id', 'money_goal']
