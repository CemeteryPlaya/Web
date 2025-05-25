from django.db import models

# Create your models here.
class Registration(models.Model):
    login = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    pickup = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.login} - {self.phone}"