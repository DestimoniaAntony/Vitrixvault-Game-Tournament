from django import forms
from django.contrib.auth.models import User
from .models import Institution
from django.contrib.auth.hashers import make_password

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



class InstitutionEditForm(forms.ModelForm):
    class Meta:
        model = Institution
        fields = ['name', 'address', 'contact_phone']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'contact_phone': forms.TextInput(attrs={'class': 'form-control'}),
        }






        