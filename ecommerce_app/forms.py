from django import forms
from django.contrib.auth.models import User
from .models import Customer
from django.core.exceptions import ValidationError

class CustomerRegistrationForm(forms.ModelForm):
    username = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Username"}
        ),
    )
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "First Name"}
        ),
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Last Name"}
        ),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Password"}
        ),
        required=True,
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Confirm Password"}
        ),
        required=True,
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "Email"}
        ),
    )

    class Meta:
        model = Customer
        fields = ["phone", "address", "profile_picture"]
        widgets = {
            "phone": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Phone"}
            ),
            "address": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Address"}
            ),
            "profile_picture": forms.ClearableFileInput(
                attrs={"class": "form-control"}
            ),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password != confirm_password:
            self.add_error("confirm_password", "Passwords do not match.")

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError("This username is already taken. Please choose another.")
        return username