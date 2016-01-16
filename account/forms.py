import ipdb

from django.contrib.auth.models import User
from django import forms
from django.contrib.auth import authenticate


class SigninForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'username', }),
            'password': forms.PasswordInput(attrs={'placeholder': 'password', }),
        }

    def __init__(self, *args, **kwargs):
        super(SigninForm, self).__init__(*args, **kwargs)
        self.fields['username'].help_text = ''
        self.fields['username'].label = ''
        self.fields['password'].label = ''
        self.error_css_class = 'error_css'
        self.required_css_class = "required"

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)

        if not user or not user.is_active:
            raise forms.ValidationError("Incorrect username or password")

        return self.cleaned_data

    def is_valid(self):
        result = super(SigninForm, self).is_valid()
        if self.errors:
            self.fields['username'].widget.attrs.update({'class':  'required_error'})
            self.fields['password'].widget.attrs.update({'class':  'required_error'})
        return result