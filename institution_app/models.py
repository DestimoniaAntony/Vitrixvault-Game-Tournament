from django.db import models

from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from staff_app.models import Institution
from django.core.exceptions import ValidationError
from django.utils import timezone
import re
# Create your models here.


class Event(models.Model):
    VISIBILITY_CHOICES = [
        (True, "Public"),
        (False, "Private"),
    ]

    name = models.CharField(max_length=255)
    date = models.DateField()
    time = models.TimeField()
    rules = models.TextField(blank=True)
    description = models.TextField(blank=True)
    location = models.CharField(max_length=255, blank=True)
    visibility = models.BooleanField(choices=VISIBILITY_CHOICES, default=True)
    max_participants = models.PositiveIntegerField(null=True, blank=True)
    team_size = models.PositiveIntegerField(default=1) 
    created_by = models.ForeignKey(Institution, on_delete=models.CASCADE)  # Staff member who created the event
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, related_name='students')
    events = models.ManyToManyField(Event, related_name='students')
    phone = models.CharField(
    max_length=15,
    validators=[
        RegexValidator(r'^\d{10,15}$', "Phone number must be 10–15 digits.")
    ]
    )
    address = models.TextField()
    date_of_birth = models.DateField()
    roll_number = models.PositiveIntegerField()
    course = models.CharField(max_length=100)
    password = models.CharField(max_length=128)  # Storing plain password for reference
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} - {self.roll_number}"
    

class Team(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="teams")
    team_number = models.PositiveIntegerField()
    members = models.ManyToManyField(Student, related_name="teams")

    def __str__(self):
        return f"Team {self.team_number} - {self.event.name}"


class Match(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    team1 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="team1_matches")
    team2 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="team2_matches")
    score_team1 = models.IntegerField(default=0)
    score_team2 = models.IntegerField(default=0)
    status = models.CharField(max_length=20, choices=[('Upcoming', 'Upcoming'), ('Ongoing', 'Ongoing'), ('Finished', 'Finished')], default='Upcoming')
    start_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.team1} vs {self.team2} ({self.status})"
    

    