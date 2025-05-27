from django.db import models
from django.contrib.auth.models import User
from Victrix_app.models import Staff
from django.contrib.auth.hashers import make_password
# Create your models here.


class Institution(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="institutions")
    name = models.CharField(max_length=255, unique=True)
    address = models.TextField()
    contact_phone = models.CharField(max_length=15)
    plain_password = models.CharField(max_length=255)  # Storing plain password
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, related_name="institutions")

    def __str__(self):
        return self.name





