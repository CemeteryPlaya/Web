from django.db import models
from django.conf import settings

# Create your models here.
class Registration(models.Model):
    login = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    pickup = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.login} - {self.phone}"
    
class TrackCode(models.Model):
    STATUS_CHOICES = [
        ('user_added', 'Добавлено пользователем'),
        ('warehouse_cn', 'Принято на склад (Китай)'),
        ('shipped_cn', 'Отправлено со склада (Китай)'),
        ('delivered', 'Доставлено на ПВЗ'),
    ]

    id = models.AutoField(primary_key=True, verbose_name="№ трек кода")
    track_code = models.CharField(max_length=100, unique=True, verbose_name="Трек код")
    update_date = models.DateField(auto_now=True, verbose_name="Дата обновления")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, verbose_name="Статус трек-кода")
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Имя владельца"
    )
    description = models.CharField(max_length=255, blank=True, verbose_name="О посылке")
    weight = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True, verbose_name="Вес посылки (кг)")

    def __str__(self):
        return f"{self.track_code} - {self.get_status_display()}"