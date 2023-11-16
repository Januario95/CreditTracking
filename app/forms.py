from django import forms

from .models import (
    Client,
)

class DateInput(forms.DateInput):
    input_type = 'date'

class MonthInput(forms.DateInput):
    input_type = 'month'


class ClientModelForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ('first_name', 'last_name', 'job_title', 'email',
                  'company', 'phone_number', 'phone_number2',
                  # 'amount_requested', 'interest_rate',
                  # 'id_document', 'contract', 
                  )

class ClientForm(forms.Form):
    first_name = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            
        })
    )
    last_name = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            
        })
    )
    job_title = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            
        })
    )
    email = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            
        })
    )
    company = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            
        })
    )
    phone_number = forms.CharField(
        max_length=12,
        widget=forms.TextInput(attrs={
            
        })
    )
    phone_number2 = forms.CharField(
        max_length=12,
        widget=forms.TextInput(attrs={
            
        })
    )
    amount_requested = forms.DecimalField(
        max_digits=10, decimal_places=2,
        widget=forms.NumberInput(attrs={
            
        })
    )
    # id_document = forms.FileField()
    # contract = forms.FileField()
    interest_rate = forms.DecimalField(
        max_digits=10, decimal_places=2,
        widget=forms.NumberInput(attrs={
            
        })
    )
    months_to_repay = forms.IntegerField(
        min_value=1,
    )
    starting_month = forms.DateField(widget=DateInput)

class InterestSimulatorForm(forms.Form):
    amount = forms.DecimalField(
        max_digits=10, decimal_places=2,
        widget=forms.NumberInput(attrs={
            'value': 10000
        })
    )
    number_of_months = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'value': 5
        })
    )
    interest_rate = forms.DecimalField(
        max_digits=10, decimal_places=2,
        widget=forms.NumberInput(attrs={
            'value': 25
        }))
    starting_month = forms.DateField(widget=DateInput)

