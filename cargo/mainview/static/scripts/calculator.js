document.addEventListener('DOMContentLoaded', () => {
  const weightInput = document.getElementById('weight');
  const inc = document.getElementById('increment');
  const dec = document.getElementById('decrement');
  const totalWeight = document.getElementById('total-weight');
  const totalPrice = document.getElementById('total-price');
  const discountEl = document.getElementById('discount'); // элемент для вывода скидки (можно добавить в HTML)
  const RATE = 1859;
  const DISCOUNT_PER_KG = 50;
  const DISCOUNT_THRESHOLD = 30;

  if (!weightInput) return;

  const update = () => {
    const w = parseFloat(weightInput.value) || 0;

    // Базовая цена без скидки
    const basePrice = w * RATE;

    // Проверяем условие скидки
    let discount = 0;
    if (w >= DISCOUNT_THRESHOLD) {
      discount = w * DISCOUNT_PER_KG;
    }

    // Итог с учётом скидки
    const finalPrice = Math.max(basePrice - discount, 0);

    // Обновляем UI
    totalWeight.textContent = `${w} кг`;
    totalPrice.textContent = `${finalPrice.toLocaleString()} ₸`;

    // Если в HTML есть элемент для отображения скидки — покажем её
    if (discountEl) {
      if (discount > 0) {
        discountEl.textContent = `Скидка: ${discount.toLocaleString()} ₸`;
        discountEl.classList.remove('hidden');
      } else {
        discountEl.textContent = '';
        discountEl.classList.add('hidden');
      }
    }
  };

  weightInput.addEventListener('input', update);

  inc?.addEventListener('click', () => {
    let w = parseFloat(weightInput.value) || 0;
    if (w < 100) weightInput.value = w + 1;
    update();
  });

  dec?.addEventListener('click', () => {
    let w = parseFloat(weightInput.value) || 0;
    if (w > 0) weightInput.value = w - 1;
    update();
  });

  update(); // первичный расчёт при загрузке
});
