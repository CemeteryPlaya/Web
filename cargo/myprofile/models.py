from django.db import models
from django.conf import settings

# Create your models here.
class TrackCode(models.Model):
    STATUS_CHOICES = [
        ('user_added', 'Добавлено пользователем'),
        ('warehouse_cn', 'Принято на склад (Китай)'),
        ('shipped_cn', 'Отправлено со склада (Китай)'),
        ('delivered', 'Доставлено на ПВЗ'),
        ('claimed', 'Выдано получателю'),
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
    weight = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True, verbose_name="Вес посылки (кг)")

    def __str__(self):
        return f"{self.track_code} - {self.get_status_display()}"
    
class Receipt(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Владелец")
    created_at = models.DateField(auto_now_add=True, verbose_name="Дата создания")
    is_paid = models.BooleanField(default=False, verbose_name="Статус оплаты")
    total_weight = models.DecimalField(max_digits=6, decimal_places=3, default=0, verbose_name="Общий вес (кг)")
    total_price = models.DecimalField(max_digits=10, decimal_places=0, default=0, verbose_name="Сумма чека")
    
    # 🏬 Пункт выдачи
    pickup_point = models.CharField(max_length=255, blank=True, null=True, verbose_name="Пункт выдачи")
    
    # 💳 Ссылка на оплату (генерируется в зависимости от пункта)
    payment_link = models.URLField(blank=True, null=True, verbose_name="Ссылка на оплату")

    def __str__(self):
        return f"Чек #{self.id} от {self.created_at} — {'Оплачен' if self.is_paid else 'Не оплачен'}"

class ReceiptItem(models.Model):
    receipt = models.ForeignKey(Receipt, related_name='items', on_delete=models.CASCADE)
    track_code = models.OneToOneField(TrackCode, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.track_code)

class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notifications")
    message = models.CharField(max_length=255, verbose_name="Сообщение")
    is_read = models.BooleanField(default=False, verbose_name="Прочитано")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата")

    def __str__(self):
        return f"Уведомление для {self.user.username}: {self.message}"
    
class CustomerDiscount(models.Model):
    """Постоянная или разовая скидка в тенге за 1 кг"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="discounts",
        verbose_name="Пользователь"
    )
    amount_per_kg = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        verbose_name="Скидка (₸/кг)"
    )
    is_temporary = models.BooleanField(default=False, verbose_name="Разовая скидка")
    active = models.BooleanField(default=True, verbose_name="Активная скидка")
    comment = models.CharField(max_length=255, blank=True, verbose_name="Комментарий")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        type_label = "Разовая" if self.is_temporary else "Постоянная"
        return f"{type_label} скидка {self.amount_per_kg} ₸/кг ({self.user.username})"
    
class UserPushSubscription(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    subscription_data = models.JSONField(default=dict, blank=True, null=True)