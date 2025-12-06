from django import forms
from django.contrib.auth.models import User
from .models import Institution
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
import re

class InstitutionForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Institution
        fields = ['username', 'email', 'password', 'name', 'address', 'contact_phone']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'contact_phone': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def save(self, commit=True):
        # Create user with hashed password
        password = self.cleaned_data['password']
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=password  # Django will automatically hash the password here
        )

        institution = Institution(
            user=user,
            name=self.cleaned_data['name'],
            address=self.cleaned_data['address'],
            contact_phone=self.cleaned_data['contact_phone'],
            plain_password=password  # Storing plain password here
        )

        if commit:
            institution.save()

        return institution

    # --- Field-level validation helpers ---
    def clean_username(self):
        username = (self.cleaned_data.get('username') or '').strip()
        if not username:
            raise ValidationError('Username is required.')
        # Allow letters, numbers, dot, underscore, hyphen; length 3-30
        if not re.match(r'^[A-Za-z0-9._-]{3,30}$', username):
            raise ValidationError('Username must be 3-30 characters and contain only letters, numbers, dot, underscore or hyphen.')
        if User.objects.filter(username=username).exists():
            raise ValidationError('This username is already taken.')
        return username

    def clean_email(self):
        email = (self.cleaned_data.get('email') or '').strip()
        if not email:
            raise ValidationError('Email is required.')
        if User.objects.filter(email=email).exists():
            raise ValidationError('An account with this email already exists.')
        return email

    def clean_password(self):
        password = self.cleaned_data.get('password') or ''
        if len(password) < 8:
            raise ValidationError('Password must be at least 8 characters long.')
        # basic strength check: letters and numbers
        if not re.search(r'[A-Za-z]', password) or not re.search(r'\d', password):
            raise ValidationError('Password must contain both letters and numbers.')
        return password

    def clean_contact_phone(self):
        phone = (self.cleaned_data.get('contact_phone') or '').strip()
        if phone == '':
            return phone
        if not re.match(r'^\d{10}$', phone):
            raise ValidationError('Contact phone must be exactly 10 digits.')
        return phone

    def clean(self):
        """Cross-field validation (if needed). Keep as a hook for future checks."""
        cleaned = super().clean()
        # No additional cross-field checks right now; return cleaned data
        return cleaned



class InstitutionEditForm(forms.ModelForm):
    class Meta:
        model = Institution
        fields = ['name', 'address', 'contact_phone']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'contact_phone': forms.TextInput(attrs={'class': 'form-control'}),
        }






        