from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)
    pickup = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.user.username} — {self.phone}"