"""
Forms for user authentication and profile management
"""
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Field
from .models import User, UserProfile

class CustomUserCreationForm(UserCreationForm):
    """
    Custom user registration form
    """
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('first_name', css_class='form-group col-md-6 mb-3'),
                Column('last_name', css_class='form-group col-md-6 mb-3'),
                css_class='form-row'
            ),
            Field('username', css_class='form-control mb-3'),
            Field('email', css_class='form-control mb-3'),
            Field('password1', css_class='form-control mb-3'),
            Field('password2', css_class='form-control mb-3'),
            Submit('submit', 'Create Account', css_class='btn btn-primary btn-lg w-100')
        )
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user

class CustomAuthenticationForm(AuthenticationForm):
    """
    Custom login form
    """
    username = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('username', css_class='form-control mb-3'),
            Field('password', css_class='form-control mb-3'),
            Submit('submit', 'Sign In', css_class='btn btn-primary btn-lg w-100')
        )

class UserProfileForm(forms.ModelForm):
    """
    Form for updating user profile
    """
    class Meta:
        model = UserProfile
        fields = ['bio', 'avatar', 'avatar_url', 'phone_number', 'date_of_birth', 'theme_preference', 
                 'email_notifications', 'desktop_notifications']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'avatar_url': forms.URLInput(attrs={'placeholder': 'https://example.com/your-avatar.jpg'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('avatar', css_class='form-control mb-3'),
            Field('avatar_url', css_class='form-control mb-3'),
            Field('bio', css_class='form-control mb-3'),
            Row(
                Column('phone_number', css_class='form-group col-md-6 mb-3'),
                Column('date_of_birth', css_class='form-group col-md-6 mb-3'),
                css_class='form-row'
            ),
            Field('theme_preference', css_class='form-control mb-3'),
            Row(
                Column('email_notifications', css_class='form-group col-md-6 mb-3'),
                Column('desktop_notifications', css_class='form-group col-md-6 mb-3'),
                css_class='form-row'
            ),
            Submit('submit', 'Update Profile', css_class='btn btn-primary')
        )

class UserUpdateForm(forms.ModelForm):
    """
    Form for updating basic user information
    """
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('first_name', css_class='form-group col-md-6 mb-3'),
                Column('last_name', css_class='form-group col-md-6 mb-3'),
                css_class='form-row'
            ),
            Field('email', css_class='form-control mb-3'),
            Submit('submit', 'Update Information', css_class='btn btn-primary')
        )
