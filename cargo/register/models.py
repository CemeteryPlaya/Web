from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
    PICKUP_CHOICES = [
        ('akbulak', 'Акбулак 21 (Ozon)'),
        ('pushkina', 'Пушкина 8 (Ozon)'),
        ('tashkentskaya', 'Ташкентская 286 (Ozon)'),
        ('abaya323', 'Абая 323 (Beer bochka)'),
        ('bayseytovoy', 'Байсеитовой 30 (Ozon)'),
        ('samal', 'Самал 48 (Wildberries)'),
        ('sorokina', 'Сорокина 7 (Ozon)'),
        ('ashimbaeva', 'Ашимбаева 5 (Ozon)'),
        ('akkozieva', 'Аккозиева 53 (Ozon)'),
        ('abaya286', 'Абая 286 (Ozon)'),
        ('atabaeva', 'Атабаева 105 (Ozon)'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Имя пользователя")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    pickup = models.CharField(max_length=100, choices=PICKUP_CHOICES, verbose_name="ПВЗ")

    def __str__(self):
        return f"{self.user.username} — {self.phone}"