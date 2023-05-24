from typing import Any, Dict, Mapping, Optional, Type, Union
from django import forms
from django.core.files.base import File
from django.db.models.base import Model
from django.forms.utils import ErrorList
from .models import *


class Insert_Amount(forms.ModelForm):
    name = forms.CharField(max_length=100, label="Nombre")
    amount = forms.DecimalField(max_digits=10, decimal_places=2, label="Cantidad $")
    done_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label="Fecha de realizado")
    transaction_type = forms.ChoiceField(choices=[(1, 'Ingreso'), (0, 'Egreso')],
                                         widget=forms.RadioSelect,
                                         required=True,
                                         label = "Tipo de movimiento")
    category = forms.ModelChoiceField(
        queryset=GeneralCategory.objects.all(),
        widget=forms.Select,
        label = "Categoria")
    description = forms.CharField(widget=forms.Textarea, label="Description")
    detained = forms.BooleanField(required=False, widget=forms.CheckboxInput, label="Detenido")
    type = forms.ModelChoiceField(
        queryset=TypeC.objects.all(),
        widget=forms.Select,
        label= "Tipo tarjeta")
    pay_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)

    class Meta:
        model = MoneyInformation
        fields = ['name', 'amount', 'done_date', 'transaction_type', 'category', 'description',
                  'detained', 'type', 'pay_date']
        

        
class Update_Moneyflow(forms.ModelForm):

    name = forms.CharField(max_length=100, label="Nombre")
    amount = forms.DecimalField(max_digits=10, decimal_places=2, label="Cantidad $")
    done_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label="Fecha de realizado")
    transaction_type = forms.ChoiceField(choices=[(1, 'Ingreso'), (0, 'Egreso')],
                                         widget=forms.RadioSelect,
                                         required=True,
                                         label = "Tipo de movimiento")
    category = forms.ModelChoiceField(
        queryset=GeneralCategory.objects.all(),
        widget=forms.Select,
        label = "Categoria")
    description = forms.CharField(widget=forms.Textarea, label="Description")
    detained = forms.BooleanField(required=False, widget=forms.CheckboxInput, label="Detenido")
    type = forms.ModelChoiceField(
        queryset=TypeC.objects.all(),
        widget=forms.Select,
        label= "Tipo tarjeta")
    pay_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = MoneyInformation
        fields = ['name', 'amount', 'done_date', 'transaction_type', 'category', 'description',
                  'detained', 'type', 'pay_date']
        
        
            
    
        
    
    
        