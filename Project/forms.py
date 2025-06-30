#from django import forms# cars/forms.py
from django import forms
from .models import Car,Order

class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['brand', 'model', 'year', 'location', 'price_per_day', 'description', 'image']

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['car', 'start_date', 'end_date']
