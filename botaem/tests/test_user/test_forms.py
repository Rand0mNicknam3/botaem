from django.test import TestCase
from user.forms import UserCreateForm, LoginForm

class TestUserCreateForm(TestCase):

    def test_email_form_label(self):
        Form = UserCreateForm()
        self.assertTrue(Form.fields['email'].label == 'Your email address')
    
    def test_email_form_required(self):
        Form = UserCreateForm()
        self.assertTrue(Form.fields['email'].required)

    def test_password_form_labels(self):
        Form = UserCreateForm()
        self.assertTrue(Form.fields['password1'].label == 'Password')
        self.assertTrue(Form.fields['password2'].label == 'Password confirmation')

    def test_password_form_placeholders(self):
        Form = UserCreateForm()
        self.assertTrue(Form.fields['password1'].widget.attrs['placeholder'] == 'Password')
        self.assertTrue(Form.fields['password2'].widget.attrs['placeholder'] == 'Confirm password')
    
    def test_email_form_placeholder(self):
        Form = UserCreateForm()
        self.assertTrue(Form.fields['email'].widget.attrs['placeholder'] == 'example@example.com')
    
    def test_username_form_placeholder(self):
        Form = UserCreateForm()
        self.assertTrue(Form.fields['username'].widget.attrs['placeholder'] == 'Username')

class TestLoginForm(TestCase):

    def test_username_max_length(self):
        Form = LoginForm()
        self.assertTrue(Form.fields['username'].max_length == 25)

    def test_password_max_length(self):
        Form = LoginForm()
        self.assertTrue(Form.fields['password'].max_length == 200)
    
    def test_password_autocomplete(self):
        Form = LoginForm()
        self.assertTrue(Form.fields['password'].widget.attrs['autocomplete'] == 'current-password')
