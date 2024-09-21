from django import forms
from . models import ShippingAddress

class ShippingForm(forms.ModelForm):

    class Meta:
        model = ShippingAddress
        fields = ['full_name', 'email', 'address', 'address_2', 'city', 'province', 'postal_code']
        exclude = ['user',]
