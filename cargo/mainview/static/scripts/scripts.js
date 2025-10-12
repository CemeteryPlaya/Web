document.addEventListener('DOMContentLoaded', function () {
    // --- Мобильное меню ---
    // Проверяем, существуют ли элементы меню, чтобы избежать ошибок на страницах без них
    const menuToggle = document.getElementById('mobile-menu-toggle');
    const menuClose = document.getElementById('mobile-menu-close');
    const mobileMenu = document.getElementById('mobile-menu');
    const mobileMenuOverlay = document.getElementById('mobile-menu-overlay');

    // Проверяем, существуют ли элементы сайдбара
    const sidebarClose = document.getElementById('mobile-sidebar-close');
    const mobileSidebar = document.getElementById('mobile-sidebar');
    const mobileSidebarOverlay = document.getElementById('mobile-sidebar-overlay');

    if (menuToggle) {
        // Определяем, аутентифицирован ли пользователь
        const isAuthenticated = menuToggle.dataset.isAuthenticated === 'true';

        function openMenu() {
            if (isAuthenticated && mobileSidebar && mobileSidebarOverlay) {
                // Открываем мобильный сайдбар для аутентифицированных пользователей
                mobileSidebar.classList.remove('hidden');
                mobileSidebarOverlay.classList.remove('hidden');
                document.body.style.overflow = 'hidden';
                // Убедимся, что стандартное меню закрыто
                if (mobileMenu) mobileMenu.classList.add('hidden');
                if (mobileMenuOverlay) mobileMenuOverlay.classList.add('hidden');
            } else if (mobileMenu && mobileMenuOverlay) {
                // Открываем стандартное мобильное меню для неаутентифицированных
                mobileMenu.classList.remove('hidden');
                mobileMenuOverlay.classList.remove('hidden');
                document.body.style.overflow = 'hidden';
                // Убедимся, что сайдбар закрыт (на всякий случай)
                if (mobileSidebar) mobileSidebar.classList.add('hidden');
                if (mobileSidebarOverlay) mobileSidebarOverlay.classList.add('hidden');
            }
        }

        function closeMenu() {
            // Закрываем стандартное меню
            if (mobileMenu) mobileMenu.classList.add('hidden');
            if (mobileMenuOverlay) mobileMenuOverlay.classList.add('hidden');
            // Закрываем сайдбар
            if (mobileSidebar) mobileSidebar.classList.add('hidden');
            if (mobileSidebarOverlay) mobileSidebarOverlay.classList.add('hidden');
            document.body.style.overflow = '';
        }

        menuToggle.addEventListener('click', openMenu);

        // Обработчики для закрытия стандартного меню
        if (menuClose) {
            menuClose.addEventListener('click', function() {
                if (mobileMenu) mobileMenu.classList.add('hidden');
                if (mobileMenuOverlay) mobileMenuOverlay.classList.add('hidden');
                document.body.style.overflow = '';
            });
        }
        if (mobileMenuOverlay) {
            mobileMenuOverlay.addEventListener('click', function() {
                mobileMenu.classList.add('hidden');
                mobileMenuOverlay.classList.add('hidden');
                document.body.style.overflow = '';
            });
        }

        // Обработчики для закрытия мобильного сайдбара
        if (sidebarClose) {
            sidebarClose.addEventListener('click', function() {
                if (mobileSidebar) mobileSidebar.classList.add('hidden');
                if (mobileSidebarOverlay) mobileSidebarOverlay.classList.add('hidden');
                document.body.style.overflow = '';
            });
        }
        if (mobileSidebarOverlay) {
            mobileSidebarOverlay.addEventListener('click', function() {
                mobileSidebar.classList.add('hidden');
                mobileSidebarOverlay.classList.add('hidden');
                document.body.style.overflow = '';
            });
        }

        // Закрытие меню/сайдбара при изменении размера окна на desktop
        window.addEventListener('resize', function() {
            if (window.innerWidth >= 768) { // md breakpoint
                closeMenu(); // Используем общую функцию закрытия
            }
        });

        // Опционально: Закрытие меню/сайдбара при нажатии Escape
        document.addEventListener('keydown', function(e) {
             if (e.key === "Escape") {
                 if ((mobileMenu && !mobileMenu.classList.contains('hidden')) ||
                     (mobileSidebar && !mobileSidebar.classList.contains('hidden'))) {
                     closeMenu();
                 }
             }
        });
    }
    // --- Конец мобильного меню ---

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

    if (weightInput) {
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
    }

    // FAQ аккордеон
    const faqToggles = document.querySelectorAll('.faq-toggle');
    faqToggles.forEach(toggle => {
        toggle.addEventListener('click', function () {
            const targetId = this.getAttribute('data-target');
            const content = document.getElementById(targetId);
            const icon = this.querySelector('i');

            content.classList.toggle('hidden');
            icon.classList.toggle('ri-arrow-down-s-line');
            icon.classList.toggle('ri-arrow-up-s-line');
        });
    });

    // Маска для телефона
    const phoneInput = document.getElementById('phone');

    const formatPhone = (value) => {
        const digits = value.replace(/\D/g, '');
        let cleaned = digits.startsWith('7') ? digits : '7' + digits;
        cleaned = cleaned.slice(0, 11);

        let result = '+7';
        if (cleaned.length > 1) result += ' (' + cleaned.substring(1, 4);
        if (cleaned.length >= 4) result += ') ' + cleaned.substring(4, 7);
        if (cleaned.length >= 7) result += '-' + cleaned.substring(7, 9);
        if (cleaned.length >= 9) result += '-' + cleaned.substring(9, 11);

        return result;
    };

    if (phoneInput) {
        // Инициализация
        if (!phoneInput.value) {
            phoneInput.value = '';
        }

        phoneInput.addEventListener('input', (e) => {
            phoneInput.value = formatPhone(e.target.value);
        });

        phoneInput.addEventListener('keydown', function (e) {
        const pos = phoneInput.selectionStart;
        const val = phoneInput.value;

        // --- BACKSPACE: если курсор «до» кода +7, блокируем,
        // и если перед курсором форматный символ, удаляем предыдущую цифру ---
        if (e.key === 'Backspace') {
            if (pos <= 3) {
                e.preventDefault();
            } else {
                // если перед курсором стоит скобка или дефис, удаляем предыдущую цифру
                const prevChar = val.charAt(pos - 1);
                if (/\D/.test(prevChar)) {
                    e.preventDefault();
                    // считаем, сколько цифр в строке до позиции (pos-1)
                    let digitCount = 0;
                    for (let i = 0; i < pos - 1; i++) {
                        if (/\d/.test(val.charAt(i))) digitCount++;
                    }
                    let digits = val.replace(/\D/g, '').split('');
                    if (digitCount > 0) {
                        // удаляем ту цифру, которая стоит «перед» форматным символом
                        digits.splice(digitCount - 1, 1);
                        phoneInput.value = formatPhone(digits.join(''));
                        // выставляем курсор чуть левее (или минимум после "+7 ")
                        const newPos = Math.max(4, pos - 1);
                        setTimeout(() => phoneInput.setSelectionRange(newPos, newPos), 0);
                    }
                }
            }
        }

        // --- DELETE: если курсор «на» скобке/дефисе, удаляем следующую цифру ---
        if (e.key === 'Delete') {
            // если на месте курсора стоит не цифра
            if (pos < val.length && /\D/.test(val.charAt(pos))) {
                e.preventDefault();
                let digits = val.replace(/\D/g, '').split('');
                // считаем, сколько цифр до этой позиции
                let digitCount = 0;
                for (let i = 0; i < pos; i++) {
                    if (/\d/.test(val.charAt(i))) digitCount++;
                }
                // если есть следующая цифра, удаляем её
                if (digitCount < digits.length) {
                    digits.splice(digitCount, 1);
                    phoneInput.value = formatPhone(digits.join(''));
                    setTimeout(() => phoneInput.setSelectionRange(pos, pos), 0);
                }
            }
            // блокируем удаление до "+7 "
            if (pos <= 3) {
                e.preventDefault();
            }
        }
    });

        phoneInput.addEventListener('paste', function (e) {
            e.preventDefault();
            const pasted = (e.clipboardData || window.clipboardData).getData('text');
            phoneInput.value = formatPhone(pasted);
        });
    }

    // Форма регистрации
    const registrationForm = document.getElementById('registration-form');

    if (registrationForm) {
        const passwordInput = document.getElementById('password');
        const confirmPasswordInput = document.getElementById('confirm-password');
        const loginInput = document.getElementById('login');
        const pickupInput = document.getElementById('pickup');

        // Проверка совпадения пароля в реальном времени
        confirmPasswordInput.addEventListener('input', function () {
            if (confirmPasswordInput.value !== passwordInput.value) {
                confirmPasswordInput.classList.add('border-red-500');
            } else {
                confirmPasswordInput.classList.remove('border-red-500');
            }
        });

        registrationForm.addEventListener('submit', function (e) {
            const login = loginInput.value.trim();
            const pickup = pickupInput.value;
            const password = passwordInput.value;
            const confirmPassword = confirmPasswordInput.value;
            const rawPhone = phoneInput.value.replace(/\D/g, '');

            let isValid = true;
            let errorMessage = '';

            // Проверка номера телефона
            if (rawPhone.length !== 11 || !rawPhone.startsWith('7')) {
                isValid = false;
                errorMessage += 'Введите корректный номер телефона в формате +7 (XXX) XXX-XX-XX\n';
            }

            // Проверка логина
            if (!login) {
                isValid = false;
                errorMessage += 'Введите логин\n';
            }

            // Проверка пункта выдачи
            if (!pickup) {
                isValid = false;
                errorMessage += 'Выберите пункт выдачи\n';
            }

            // Проверка пароля
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
                e.preventDefault();
                alert('Пожалуйста, исправьте следующие ошибки:\n' + errorMessage);
            } else {
                phoneInput.value = formatPhone(rawPhone);
            }
        });
    }

    // Форма логина
    const loginForm = document.getElementById('login-form');

    if (loginForm) {
        const loginInput = document.getElementById('login');
        const passInput = document.getElementById('password');

        loginForm.addEventListener('submit', function (e) {
            const login = loginInput.value.trim();
            const password = passInput.value;

            let isValid = true;
            let errorMessage = '';

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
    }

        // --- Выпадающее меню уведомлений ---
    const notifButton = document.getElementById('notification-button');
    const notifDropdown = document.getElementById('notification-dropdown');

    if (notifButton && notifDropdown) {
        // Переключение выпадашки
        notifButton.addEventListener('click', function (e) {
            e.stopPropagation(); // чтобы клик не дошел до window
            notifDropdown.classList.toggle('hidden');
        });

        // Клик вне выпадашки — закрываем
        window.addEventListener('click', function (e) {
            if (!notifDropdown.contains(e.target) && !notifButton.contains(e.target)) {
                notifDropdown.classList.add('hidden');
            }
        });

        // Escape тоже закрывает
        document.addEventListener('keydown', function (e) {
            if (e.key === "Escape") {
                notifDropdown.classList.add('hidden');
            }
        });
    }
});
