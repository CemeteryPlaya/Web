from django.shortcuts import render, redirect
from .models import Registration

# Create your views here.
def index(request):
    return render(request, "index.html")

def education(request):
    return render(request, "education.html")

def register_view(request):
    if request.method == 'POST':
        login = request.POST.get('login')
        phone = request.POST.get('phone')
        pickup = request.POST.get('pickup')

        # Проверка вывода в консоль
        print("Получены данные:", login, phone, pickup)

        if login and phone and pickup:
            Registration.objects.create(
                login=login,
                phone=phone,
                pickup=pickup
            )
            return redirect('success')  # создайте такую страницу
        else:
            return render(request, 'index.html', {
                'error': 'Заполните все поля корректно.'
            })

    return render(request, 'index.html')

def success_view(request):
    return render(request, 'success.html')