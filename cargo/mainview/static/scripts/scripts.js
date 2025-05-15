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

    phoneInput.addEventListener('input', function (e) {
        let value = e.target.value.replace(/\D/g, '');

        if (value.length > 10) {
            value = value.slice(0, 10);
        }

        let formattedValue = '';

        if (value.length > 0) {
            formattedValue += '(' + value.substring(0, 3);
        }

        if (value.length > 3) {
            formattedValue += ') ' + value.substring(3, 6);
        }

        if (value.length > 6) {
            formattedValue += ' - ' + value.substring(6, 8);
        }

        if (value.length > 8) {
            formattedValue += ' - ' + value.substring(8, 10);
        }

        e.target.value = formattedValue;
    });

    // Форма регистрации
    const registrationForm = document.getElementById('registration-form');

    registrationForm.addEventListener('submit', function (e) {
        const login = document.getElementById('login').value;
        const phone = document.getElementById('phone').value;
        const pickup = document.getElementById('pickup').value;

        let isValid = true;
        let errorMessage = '';

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

        if (!isValid) {
            e.preventDefault(); // Оставляем здесь только при ошибке
            alert('Пожалуйста, исправьте следующие ошибки:\n' + errorMessage);
        }
        // Если ошибок нет — форма отправляется стандартным методом POST
    });
});
