# Generated by Django 5.0.4 on 2025-06-19 17:41

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(max_length=20, verbose_name='Телефон')),
                ('pickup', models.CharField(choices=[('akbulak', 'Акбулак 21 (Ozon)'), ('pushkina', 'Пушкина 8 (Ozon)'), ('tashkentskaya', 'Ташкентская 286 (Ozon)'), ('abaya323', 'Абая 323 (Beer bochka)'), ('bayseytovoy', 'Байсеитовой 30 (Ozon)'), ('samal', 'Самал 48 (Wildberries)'), ('sorokina', 'Сорокина 7 (Ozon)'), ('ashimbaeva', 'Ашимбаева 5 (Ozon)'), ('akkozieva', 'Аккозиева 53 (Ozon)'), ('abaya286', 'Абая 286 (Ozon)'), ('atabaeva', 'Атабаева 105 (Ozon)')], max_length=100, verbose_name='ПВЗ')),
                ('is_staff', models.BooleanField(default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Имя пользователя')),
            ],
        ),
    ]
