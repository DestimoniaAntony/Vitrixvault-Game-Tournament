from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=10, blank=True)
    address = models.CharField(max_length=255, blank=True)
    password = models.CharField(max_length=128)  
    is_active = models.BooleanField(default=False)  
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
    



    