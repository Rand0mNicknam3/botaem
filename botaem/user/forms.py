from django import forms
from django.forms.widgets import TextInput
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from allauth.socialaccount.forms import SignupForm
from allauth.account.forms import SetPasswordField, PasswordField
from user.models import CustomUser

class UserCreateForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')
        
    def __init__(self, *args, **kwargs):
        super(UserCreateForm, self).__init__(*args, **kwargs)

        self.fields['email'].label = 'Your email address'
        self.fields['password1'].label = 'Password'
        self.fields['password2'].label = 'Password confirmation'
        self.fields['email'].required = True
        self.fields['password1'].help_text = ''
        self.fields['password2'].help_text = ''
        # widgets
        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'example@example.com'
        })
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Username'
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirm password'
        })


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput(attrs={'class': 'form-control'}), max_length=25)
    password = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password"}),
        max_length=200,
    )

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update({
            'placeholder': 'Username'
        })
        self.fields['password'].widget.attrs.update({
            'placeholder': 'Password'
        })

class CompleteSignUpForm(AuthenticationForm):
    password1 = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password"}),
        max_length=200,
    )
    password2 = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password"}),
        max_length=200,
    )
    def is_valid(self):
        valid = super(CompleteSignUpForm, self).is_valid()
        if self.cleaned_data['password'] != self.cleaned_data['password2']:
            self.add_error('password2', "Passwords don't match")
            return None
        return valid


class SocialPasswordedSignupForm(SignupForm):

    username = forms.CharField(widget=TextInput(attrs={'class': 'form-control'}), max_length=25)
    password1 = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password", 'class': 'form-control'}),
        max_length=200,
    )
    password2 = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password", 'class': 'form-control'}),
        max_length=200,
    )
    def __init__(self, *args, **kwargs):
        super(SocialPasswordedSignupForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
        })
        self.fields['password1'].label = 'Password'
        self.fields['password2'].label = 'Password confirmation'

    def clean_password2(self):
        if ("password1" in self.cleaned_data and "password2" in self.cleaned_data):
            if (self.cleaned_data["password1"] != self.cleaned_data["password2"]):
                raise forms.ValidationError(("You must type the same password each time."))
        return self.cleaned_data["password2"]

    def signup(self, request, user):
        user.set_password(self.cleaned_data["password1"])
        user.save()