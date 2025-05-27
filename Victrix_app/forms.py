from django import forms
from django.contrib.auth.models import User
from .models import Staff
from django.contrib.auth.forms import AuthenticationForm


class StaffRegistrationForm(forms.ModelForm):
    # Fields for User model
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))

    # Fields for Staff model
    phone = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    address = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Staff
        fields = ['phone', 'address', 'password']

    def save(self, commit=True):
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password']  # This is securely stored in User model
        )

        staff = super().save(commit=False)
        staff.user = user
        staff.password = self.cleaned_data['password']  # Store plain password in Staff table

        if commit:
            staff.save()

        return staff


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))



