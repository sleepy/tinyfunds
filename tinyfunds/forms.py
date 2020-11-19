from django import forms
from .models import Event
from datetime import datetime
from tempus_dominus.widgets import DatePicker, TimePicker, DateTimePicker
    
class CreateEventForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CreateEventForm, self).__init__(*args, **kwargs)
        self.fields['money_goal'].widget.attrs['min'] = 0

    class Meta:
        model = Event
        fields = ['title', 'org_name', 'description', 'pic', 'date', 'address', 'money_goal', 'owner_id', 'money_goal']
        widgets = {
            'date': DateTimePicker(
                options={
                    'inLine': True,
                    'useCurrent': True,
                    'collapse': False,
                    'sideBySide': True,
                    'format': 'MM/DD/YYYY HH:mm',
                },
                attrs={
                    'append': 'fa fa-calendar',
                    'icon_toggle': True,
                }
            ),
        }
