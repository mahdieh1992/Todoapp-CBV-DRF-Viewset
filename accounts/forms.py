from django import forms
from .models import User
from django.core.exceptions import ValidationError


class LoginUserForm(forms.Form):
    email = forms.CharField(widget=forms.EmailInput(attrs={"class": "form-control"}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control"})
    )


class RegisterUserForm(forms.ModelForm):
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "ConfirmPassword"}
        )
    )

    class Meta:
        model = User
        fields = ("email", "password", "password1")

        widgets = {
            "email": forms.EmailInput(
                attrs={"class": "form-control", "placeholder": "Email"}
            ),
            "password": forms.PasswordInput(
                attrs={"class": "form-control", "placeholder": "Password"}
            ),
        }

    def clean(self):
        password = self.cleaned_data["password"]
        password1 = self.cleaned_data["password1"]

        if password != password1:
            raise ValidationError("Password is not match", code=1)
