from django import forms
import csv
from django.http import HttpResponse
from .models import Stock, Accessories

class StockForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):                                                        # used to set css classes to the various fields
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'textinput form-control faded-text', 'value': ' '})
        self.fields['code'].widget.attrs.update({'class': 'textinput form-control'})
        self.fields['units'].widget.attrs.update({'class': 'textinput form-control'})
        self.fields['quantity'].widget.attrs.update({'class': 'form-control', 'min': '0'})
        self.fields['value'].widget.attrs.update({'class': 'textinput form-control'})
        self.fields['receive'].widget.attrs.update({'class': 'textinput form-control'})


    


    class Meta:
        model = Stock
        fields = ['name', 'code', 'units', 'quantity', 'value', 'receive']



class AccessoriesForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):                                                        # used to set css classes to the various fields
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'textinput form-control faded-text', 'value': ' '})
        self.fields['size'].widget.attrs.update({'class': 'textinput form-control'})
        self.fields['quantity'].widget.attrs.update({'class': 'textinput form-control', 'min': '0'})
        self.fields['value'].widget.attrs.update({'class': 'textinput form-control'})
        self.fields['receive'].widget.attrs.update({'class': 'textinput form-control'})

        

    class Meta:
        model = Accessories
        fields = ['name', 'size', 'quantity', 'value', 'receive']        