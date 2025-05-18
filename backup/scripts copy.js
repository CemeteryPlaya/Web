document.addEventListener('DOMContentLoaded', function () {
    // Калькулятор
    const weightInput = document.getElementById('weight');
    const incrementBtn = document.getElementById('increment');
    const decrementBtn = document.getElementById('decrement');
    const totalWeight = document.getElementById('total-weight');
    const totalPrice = document.getElementById('total-price');
    const RATE = 1859;

    function updateCalculation() {
        const weight = parseFloat(weightInput.value) || 0;
        const price = weight * RATE;

        totalWeight.textContent = `${weight} кг`;
        totalPrice.textContent = `${price.toLocaleString()} ₸`;
    }

    weightInput.addEventListener('input', updateCalculation);

    incrementBtn.addEventListener('click', function () {
        const currentValue = parseFloat(weightInput.value) || 0;
        if (currentValue < 100) {
            weightInput.value = currentValue + 1;
            updateCalculation();
        }
    });

    decrementBtn.addEventListener('click', function () {
        const currentValue = parseFloat(weightInput.value) || 0;
        if (currentValue > 0) {
            weightInput.value = currentValue - 1;
            updateCalculation();
        }
    });

    // FAQ аккордеон
    const faqToggles = document.querySelectorAll('.faq-toggle');

    faqToggles.forEach(toggle => {
        toggle.addEventListener('click', function () {
            const targetId = this.getAttribute('data-target');
            const content = document.getElementById(targetId);

            if (content.classList.contains('hidden')) {
                content.classList.remove('hidden');
                this.querySelector('i').classList.remove('ri-arrow-down-s-line');
                this.querySelector('i').classList.add('ri-arrow-up-s-line');
            } else {
                content.classList.add('hidden');
                this.querySelector('i').classList.remove('ri-arrow-up-s-line');
                this.querySelector('i').classList.add('ri-arrow-down-s-line');
            }
        });
    });

    // Маска для телефона
   const phoneInput = document.getElementById('phone');

    if (!phoneInput) return; // На случай, если на странице нет поля телефона

    const formatPhone = (value) => {
        const digits = value.replace(/\D/g, '');

        // Удалим лишнее
        let cleaned = digits.startsWith('7') ? digits : '7' + digits;
        cleaned = cleaned.slice(0, 11);

        let result = '+7';

        if (cleaned.length > 1) {
            result += ' (' + cleaned.substring(1, 4);
        }
        if (cleaned.length >= 4) {
            result += ') ' + cleaned.substring(4, 7);
        }
        if (cleaned.length >= 7) {
            result += '-' + cleaned.substring(7, 9);
        }
        if (cleaned.length >= 9) {
            result += '-' + cleaned.substring(9, 11);
        }

        return result;
    };

    // Инициализация
    phoneInput.value = formatPhone(phoneInput.value || '');

    // Обработка ввода
    phoneInput.addEventListener('input', (e) => {
        const value = e.target.value;
        const formatted = formatPhone(value);
        phoneInput.value = formatted;
    });

    // Защита от удаления +7
    phoneInput.addEventListener('keydown', function (e) {
        if (phoneInput.selectionStart <= 3 && (e.key === 'Backspace' || e.key === 'Delete')) {
            e.preventDefault();
        }
    });

    // Поддержка вставки
    phoneInput.addEventListener('paste', function (e) {
        e.preventDefault();
        const pasted = (e.clipboardData || window.clipboardData).getData('text');
        const digits = pasted.replace(/\D/g, '');
        phoneInput.value = formatPhone(digits);
    });

    // Форма регистрации
    const registrationForm = document.getElementById('registration-form');

    const passwordInput = document.getElementById('password');
    const confirmPasswordInput = document.getElementById('confirm_password');
    const raw = phoneInput.value.replace(/\D/g, '');

  // Проверка совпадения пароля в реальном времени
    confirmPasswordInput.addEventListener('input', function () {
        if (confirmPasswordInput.value !== passwordInput.value) {
          confirmPasswordInput.classList.add('border-red-500');
        } else {
            confirmPasswordInput.classList.remove('border-red-500');
        }
    });

    registrationForm.addEventListener('submit', function (e) {
        const login = document.getElementById('login').value;
        const phone = phoneInput.value.replace(/\D/g, '');
        const pickup = document.getElementById('pickup').value;
        const password = document.getElementById('password').value;
        const confirmPassword = document.getElementById('confirm-password').value;

        let isValid = true;
        let errorMessage = '';

        phoneInput.value = '+7' + raw.substring(1);

        if (raw.length !== 12 || !raw.startsWith('7')) {
            e.preventDefault();
            alert('Введите корректный номер телефона');
        }

        if (phone.length !== 12 || !phone.startsWith('7')) {
            e.preventDefault();
            alert('Введите корректный номер телефона в формате +7 (XXX) XXX-XX-XX');
            return;
        }

        if (!login) {
            isValid = false;
            errorMessage += 'Введите логин\n';
        }

        if (!phone || phone.length < 14) {
            isValid = false;
            errorMessage += 'Введите корректный номер телефона\n';
        }

        if (!pickup) {
            isValid = false;
            errorMessage += 'Выберите пункт выдачи\n';
        }

        if (!password || password.length < 6) {
            isValid = false;
            errorMessage += 'Пароль должен содержать минимум 6 символов\n';
        }

        if (password !== confirmPassword) {
            isValid = false;
            confirmPasswordInput.classList.add('border-red-500');
            errorMessage += 'Пароли не совпадают\n';
        }

        if (!isValid) {
            e.preventDefault(); // Оставляем здесь только при ошибке
            alert('Пожалуйста, исправьте следующие ошибки:\n' + errorMessage);
        }
        // Если ошибок нет — форма отправляется стандартным методом POST
    });

    const loginForm = document.getElementById('login-form');

    const loginInput = document.getElementById('login');
    const passInput = document.getElementById('password');

    loginForm.addEventListener('submit', function (e) {
        const login = loginInput.value.trim();
        const password = passInput.value;

        let isValid = true;
        let errorMessage = '';

        // Очистка от предыдущих ошибок
        loginInput.classList.remove('border-red-500');
        passInput.classList.remove('border-red-500');

        if (!login) {
        isValid = false;
        loginInput.classList.add('border-red-500');
        errorMessage += 'Введите логин\n';
        }

        if (!password) {
        isValid = false;
        passInput.classList.add('border-red-500');
        errorMessage += 'Введите пароль\n';
        }

        if (!isValid) {
        e.preventDefault();
        alert('Пожалуйста, исправьте следующие ошибки:\n' + errorMessage);
        }
    });


});
