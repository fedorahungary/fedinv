from django import forms

from event.models import InvEvent

class EventForm(forms.ModelForm):
	class Meta:
		model = InvEvent
		fields = ['name', 'time_from', 'time_until']
