from django import forms
from .models import *
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import ModelForm



class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['host', 'participants']


class UserForm(ModelForm):
    class Meta:
        model = User
        #fields = ['first_name', 'last_name', 'username', 'email']
        fields = ['first_name', 'last_name',  'email']



class school_databaseForm(forms.ModelForm):
    class Meta:
        model = genz_database
        fields = '__all__'  # You can specify fields explicitly if needed
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
        }



class RegisterForm(forms.Form):
    username = forms.CharField(max_length=100)
    identification_number = forms.CharField(max_length=20)
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        identification_number = cleaned_data.get('identification_number')

        if username and identification_number:
            try:
                staff = genz_database.objects.get(username=username, identification_number=identification_number)
            except genz_database.DoesNotExist:
                raise ValidationError('The provided username (Surname) and Reg No do not match.')

        return cleaned_data