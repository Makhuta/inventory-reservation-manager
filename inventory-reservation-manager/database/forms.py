from django import forms
from .models import Item, Client, Reservation


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'inventory_number', 'image', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'inventory_number': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['name', 'phone', 'email']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter full name'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter phone number'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email address'}),
        }
        labels = {
            'name': 'Full Name',
            'phone': 'Phone Number',
            'email': 'Email Address',
        }

class CSVUploadForm(forms.Form):
    csv_file = forms.FileField(label='Upload CSV file')

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['item', 'client', 'start', 'end']
        widgets = {
            'start': forms.DateInput(attrs={'type': 'date', 'class': 'form-control custom-date'}),
            'end': forms.DateInput(attrs={'type': 'date', 'class': 'form-control custom-date'}),
            'item': forms.Select(attrs={'class': 'form-control'}),
            'client': forms.Select(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super(ReservationForm, self).__init__(*args, **kwargs)
        self.fields['item'].label = 'Select Item'
        self.fields['client'].label = 'Select Client'
        self.fields['start'].label = 'Start Date and Time'
        self.fields['end'].label = 'End Date and Time'
        self.fields['start'].help_text = 'Please choose a start date'
        self.fields['end'].help_text = 'Please choose an end date'
