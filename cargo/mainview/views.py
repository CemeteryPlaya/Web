from django.shortcuts import render, redirect
from .models import Registration
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password

# Create your views here.
def index(request):
    return render(request, "index.html")

def education(request):
    return render(request, "education.html")

def pre_register(request):
    if request.method == 'POST':
        login = request.POST.get('login')
        phone = request.POST.get('phone')
        pickup = request.POST.get('pickup')

        if not all([login, phone, pickup]):
            return render(request, 'index.html', {
                'error': 'Пожалуйста, заполните все поля.',
                'login': login,
                'phone': phone,
                'pickup': pickup
            })

        # Сохраняем данные во временную сессию
        request.session['registration_data'] = {
            'login': login,
            'phone': phone,
            'pickup': pickup
        }
        return redirect('continue_register')  # это URL для registration.html

    return render(request, 'index.html')

def continue_register(request):
    data = request.session.get('registration_data')
    if not data:
        return render(request, 'index.html')  # если данных нет — на главную

    return render(request, 'registration.html', {
        'login': data.get('login', ''),
        'phone': data.get('phone', ''),
        'pickup': data.get('pickup', ''),
    })

def register_view(request):
    if request.method == 'POST':
        login = request.POST.get('login')
        phone = request.POST.get('phone')
        pickup = request.POST.get('pickup')
        password = request.POST.get('password')

        if all([login, phone, pickup, password]):
            hashed_password = make_password(password)

            Registration.objects.create(
                login=login,
                phone=phone,
                pickup=pickup,
                password=hashed_password  # сохраняем хеш
            )
            request.session.pop('registration_data', None)
            return redirect('success')
        else:
            return render(request, 'registration.html', {
                'login': login,
                'phone': phone,
                'pickup': pickup,
                'error': 'Заполните все поля корректно.'
            })

    return redirect('register')

def login_view(request):
    if request.method == 'POST':
        login = request.POST.get('login')
        password = request.POST.get('password')

        # Найти пользователя по логину
        try:
            user = Registration.objects.get(login=login)
        except Registration.DoesNotExist:
            return render(request, 'login.html', {
                'error': 'Неверный логин или пароль'
            })

        # Проверить хешированный пароль
        if check_password(password, user.password):
            # Авторизация успешна
            request.session['user_id'] = user.id  # например, сохраняем ID пользователя в сессии
            return redirect('profile')  # перенаправление на защищённую страницу
        else:
            return render(request, 'login.html', {
                'error': 'Неверный логин или пароль'
            })

    return render(request, 'login.html')

def success_view(request):
    return render(request, 'success.html')

def registartion(request):
    return render(request, "registration.html")

def profile(request):
    return render(request, "profile.html")