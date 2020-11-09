from django import forms
from .models import Event
from tempus_dominus.widgets import DatePicker, TimePicker, DateTimePicker

class DateForm(forms.Form):
    date = forms.DateTimeField(input_formats=['%d/%m/%Y %H:%M'])
    
class CreateEventForm(forms.ModelForm):

    class Meta:
        model = Event
        fields = ['title', 'org_name', 'event_date', 'description', 'pic', 'owner_id', 'address']
