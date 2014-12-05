from django import forms

class OrderForm(forms.Form):
	amount = forms.IntegerField()
