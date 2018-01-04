from django import forms
from django.contrib.auth import (authenticate, get_user_model, login, logout)


class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    # this method is executed when form.is_valid method is called
    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        user = authenticate(username=username, password=password)
        if not user:
            raise forms.ValidationError("This user doesn't exist")

        if not user.check_password(password):
            raise forms.ValidationError("Password incorrect")

        if not user.is_active:
            raise forms.ValidationError("This user is no longer active")

        return super(UserLoginForm, self).clean(*args, **kwargs)
