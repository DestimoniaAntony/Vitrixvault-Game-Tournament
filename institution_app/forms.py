from django import forms
from django.contrib.auth.models import User
from .models import Event, Student, Match


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'date', 'time', 'rules', 'description', 'location', 'visibility', 'team_size','max_participants']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'rules': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'max_participants': forms.NumberInput(attrs={'class': 'form-control'}),
            'visibility': forms.Select(attrs={'class': 'form-control'}),
            'team_size': forms.NumberInput(attrs={'class': 'form-control'}),
        }



class StudentRegistrationForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    phone = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    address = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}))
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    roll_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    course = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    event = forms.ModelMultipleChoiceField(
        queryset=Event.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # Allow multiple selection
        required=True
    )

    class Meta:
        model = Student
        fields = ['event', 'username', 'first_name', 'last_name', 'email', 'phone', 'address', 'date_of_birth', 'roll_number', 'course', 'password']

    def __init__(self, *args, **kwargs):
        institution = kwargs.pop('institution', None)
        student_instance = kwargs.get('instance', None)  # Check if instance is passed (for editing)

        super().__init__(*args, **kwargs)

        if student_instance:

            self.fields['event'].initial = student_instance.events.all()
            # If the form is used for editing, disable certain fields
            self.fields['first_name'].initial = student_instance.user.first_name
            self.fields['last_name'].initial = student_instance.user.last_name
            self.fields['email'].initial = student_instance.user.email  # Ensure email is also populated



        if institution:
            # Show all events for selection
            self.fields['event'].queryset = Event.objects.filter(created_by=institution)

        if student_instance:
            # If the form is used for editing, disable certain fields
            self.fields['username'].disabled = True
            self.fields['username'].required = False 
            self.fields['email'].disabled = True
            self.fields['email'].required = False 
            self.fields['password'].disabled = True
            self.fields['password'].required = False  # Don't make password required during editing





class MatchScoreForm(forms.ModelForm):
    class Meta:
        model = Match
        fields = ['score_team1', 'score_team2', 'status']
        widgets = {
            'score_team1': forms.NumberInput(attrs={'class': 'form-control'}),
            'score_team2': forms.NumberInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }