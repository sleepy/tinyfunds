from django import forms
from .models import Event

class DateForm(forms.Form):
    date = forms.DateTimeField(input_formats=['%d/%m/%Y %H:%M'])

class CreateEventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'org_name', 'event_date', 'description']
        