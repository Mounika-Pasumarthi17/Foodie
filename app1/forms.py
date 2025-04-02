from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm


class CustomUserCreationForm(UserCreationForm):
    phone_number = forms.CharField(max_length=15, required=True,error_messages={"required": "Phone number is required!"})
    profile_picture = forms.ImageField(required=True)

    class Meta:
        model = CustomUser
        fields = ["username", "first_name", "last_name", "email", "phone_number", "profile_picture", "password1", "password2"]


    def clean_phone_number(self):
        phone = self.cleaned_data.get("phone_number")
        if not phone.isdigit():
            raise forms.ValidationError("Phone number must contain only digits.")
        if len(phone) < 10:
            raise forms.ValidationError("Phone number must be at least 10 digits long.")
        return phone

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if not email:
            raise forms.ValidationError("Email is required!")
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("Email is already in use.")
        return email




class LoginForm(forms.Form):
    username = forms.CharField(max_length=100,required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',            
        }),
        error_messages={'required': 'Username is required'}
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
        }),
        required=True,
        error_messages={'required': 'Password is required'}
    )


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['date', 'time', 'guests', 'special_request']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
            'guests': forms.NumberInput(attrs={'min': 1}),
        }

class ShowBookingForm(forms.ModelForm):
    class Meta:
        model = ShowBooking
        fields = ['name', 'email', 'phone','date','time', 'seats']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
             'time': forms.TimeInput(attrs={'type': 'time'}),
        }

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'message']



class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class PasswordResetForm(forms.Form):
    email = forms.EmailField()

class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(label="Email", max_length=254)

class CustomSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(label="New password", widget=forms.PasswordInput)
    new_password2 = forms.CharField(label="Confirm new password", widget=forms.PasswordInput)
