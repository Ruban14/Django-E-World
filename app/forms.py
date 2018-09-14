from django import forms
from .models import Products, Address


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Products
        fields = ('name', 'description', 'price', 'image', 'category')


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ('address', 'mobile', 'email', 'postcode')
