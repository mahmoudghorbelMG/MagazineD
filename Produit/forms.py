

from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
   
    
    price = forms.DecimalField(max_digits=10, decimal_places=2, widget=forms.TextInput(attrs={'type': 'number'}))
   
    

    class Meta:
        model = Product
        fields = ['Product_name', 'price', 'description', 'brand', 'quantity_in_stock','series']
