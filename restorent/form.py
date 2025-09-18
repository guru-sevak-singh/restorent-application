from typing import Any, Mapping
from django import forms
from django.core.files.base import File
from django.db.models.base import Model
from django.forms.utils import ErrorList
from .models import FoodItem, FoodCategory, Payment, Restorent, Tax

class FoodItemForm(forms.ModelForm):
    class Meta:
        model = FoodItem
        fields = ['catogary', 'food_type', 'name', 'food_image', 'price', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'catogary': forms.Select(attrs={'class': 'form-control'}),
            'food_type': forms.Select(attrs={"class": 'form-control'}),
            'food_image': forms.FileInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': '10', 'cols': '3', 'style': 'height: 10vh'})
        }


class PaymentForm(forms.ModelForm):
    adjustment = forms.DecimalField (
        max_digits=10,
        decimal_places=2,
        required=True,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Payment
        fields = ['adjustment', 'paid_amount', 'payment_method', 'message']
        widgets = {
            'paid_amount': forms.NumberInput(attrs={'class': 'form-control', 'readonly':'readonly'}),
            'payment_method': forms.Select(attrs={'class': 'form-control'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': '3'}),
        }
    
    def __init__(self, *args, **kwargs):
        order = kwargs.pop('order', None)
        super(PaymentForm, self).__init__(*args, **kwargs)
        if order:
            self.fields['adjustment'].initial = order.adjustment

class UpdateRestorentDetail(forms.ModelForm):
    class Meta:
        model = Restorent
        fields = ['name', 'owner_name', 'address', 'upi_id', 'notification_token', 'type']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'owner_name': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'upi_id': forms.TextInput(attrs={'class': 'form-control'}),
            'notification_token': forms.TextInput(attrs={'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-control'})
        }

class AddTax(forms.ModelForm):
    class Meta:
        model = Tax
        fields = ['name', 'tax_perscentage']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'tax_perscentage': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class RestorentForm(forms.Form):
    restorent_name = forms.CharField(
        max_length=100,
        label='Restaurent Name',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    address = forms.CharField(
        label='Restaurent Address',
        widget=forms.Textarea(attrs={'class': 'form-control'})
    )
    name = forms.CharField(
        label='Owner Name',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    phone_number = forms.CharField(
        max_length=15,
        label='Phone Number',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )