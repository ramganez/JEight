import ipdb

from django.contrib.auth.models import User
from django import forms
from django.contrib.auth import authenticate


class SigninForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'username', 'class': 'foo-class'}),
            'password': forms.PasswordInput(attrs={'placeholder': 'password', 'class': 'foo-class'}),
        }

    def __init__(self, *args, **kwargs):
        super(SigninForm, self).__init__(*args, **kwargs)
        self.fields['username'].help_text = ''
        self.fields['username'].label = ''
        self.fields['password'].label = ''
        self.error_css_class = 'error_css'

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)

        if not user or not user.is_active:
            raise forms.ValidationError("Incorrect username or password")

        return self.cleaned_data