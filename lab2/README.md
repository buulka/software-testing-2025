Университет: **ITMO University**

Факультет: **FICT**

Курс: **Software Testing**

Год: **2025/2026**

Группа: **K3323**

Автор: **Ivanova Ekaterina Andreevna**

Ссылка на репозиторий: **https://github.com/buulka/software-testing-2025/tree/main/lab2**

---

## Лабораторная работа 2. Integration Tests

### 1. Описание проекта

**Проект**: 

В качестве объекта тестирования выбрано Django-приложение, реализующее работу с заказами, товарами и скидками, а также интеграцию с внешним платёжным сервисом Stripe

Пользователь может просматривать товары, создавать заказы, применять скидки и переходить к оплате через Stripe Checkout

**Выбор проекта**

Проект содержит несколько слоёв и модулей, которые активно взаимодействуют между собой:

- бизнес-логика формирования заказа;

- модуль работы с внешним API сервиса Stripe;

- уровень views, использующий бизнес-логику и базу данных.

Также, в проекте есть зависимость от внешнего сервиса, что позволяет проверить работу с API

**Модули и сервисы**:

- stripeApp.models - x ранение сущностей Item, Order, Discount;
- stripeApp.logic	- формирование данных заказа, подсчёт итоговой стоимости, применение скидок;
- stripeApp.views	- HTTP-эндпоинты для отображения заказов и создания Stripe-сессии;
- stripeApp.stripe_client	- rлиент для запросов к Stripe API;
- Stripe API	- внешний сервис обработки платежей.

### 2. Анализ взаимодействий

**Ключевые точки интеграции**:

- Views и бизнес-логика

  - views.show_order_list_page вызывает logic.get_order_data;

  Качество взаимодействия важно, потому что ошибки в бизнес-логике приводят к неправильному отображению данных для пользователя.

- Бизнес-логика и БД

  - logic.get_order_data агрегирует товары заказа, рассчитывает стоимость и процент скидки;

  Тут критична корректность расчётов.

- Views, Stripe Client и Stripe API

  - create_session_api формирует и отправляет запрос на создание платежной сессии;

  - create_coupon_api создаёт скидочный купон;

  Здесь ошибки могут полностью заблокировать процесс оплаты.

**Сценарии взаимодействия, которые отражают реальные пользовательские кейсы**:

- Просмотр заказов (пользователь открывает список заказов и view получает данные через бизнес-логику)
  
- Создание купона (пользователь вводит процент скидки, Stripe создаёт купон и id сохраняется в БД)
  
- Оплата заказа (формируется Stripe Checkout session и пользователь переходит на страницу оплаты)

### 3. Примеры написанных тестов

- Создание заказа
  
  ```python
  def create_sample_order(self):
    i1 = Item.objects.create(title='T-shirt', price=1500) 
    i2 = Item.objects.create(title='Mug', price=750)
    
    d = Discount.objects.create(coupon_id='erjnwvu', output_amount=10)
    
    order = Order.objects.create(discount_coupon=d)
    order.items.add(i1, i2)
    order.save()
    
    return order
  ```

- Бизнес-логика и БД

  ```python
  def test_get_order_data_success(self):
    order = self.create_sample_order()
    data = logic.get_order_data(order.id)

    assert data is not None
    assert data['id'] == order.id
    assert any(item['title'] == 'T-shirt' for item in data['items'])

    assert data['num_price'] == 2250
    assert data['percent'] == 10
  ```

- Несуществующий заказ (граничный случай)

  ```python
  def test_get_order_data_nonexistent(self):
    data = logic.get_order_data(999999)
    assert data is None
  ```
  
- Отображение списка заказов
  
  ```python
  def test_show_order_list_page_renders(self):
    order = self.create_sample_order()
    response = self.client.get('/')
  
    self.assertEqual(response.status_code, 200)
  
    content = response.content.decode('utf-8')
    self.assertIn('T-shirt', content)
  ```
  
- Мок интеграции с внешним API Stripe
  
  ```python
  @patch('stripeApp.stripe_client.stripe')
  def test_create_coupon_api_success_and_failure(self, mock_stripe_module):
    mock_stripe_module.Coupon.create.return_value = {'id': 'cp_test_123'}
    new_id = stripe_client.create_coupon_api(25)
    self.assertEqual(new_id, 'cp_test_123')

    mock_stripe_module.Coupon.create.side_effect = Exception('stripe error')
    new_id2 = stripe_client.create_coupon_api(50)
    self.assertIsNone(new_id2)
  ```
  
- Проверка API создания платежной сессии
  
  ```python
  @patch('stripeApp.stripe_client.stripe')
  def test_create_session_api_success_and_exception(self, mock_stripe_module):
    order = self.create_sample_order()
    order_dict = logic.get_order_data(order.id)

    mock_stripe_module.checkout.Session.create.return_value = {'url': 'https://checkout.test/session/1'}
    url = stripe_client.create_session_api(order_dict)
    self.assertIsNotNone(url)
    assert url.startswith('https://')
    
    mock_stripe_module.checkout.Session.create.side_effect = Exception('network')
    url2 = stripe_client.create_session_api(order_dict)
    self.assertIsNone(url2)
  ```
  

### 4. Результаты запуска тестов и метрика code coverage
- Все тесты были успешно выполнены;
- Ошибки Stripe корректно обрабатываются, методы возвращают None, что предотвращает падение приложения;
- Покрытие кода по модулю logic и stripe_client превышает 80%;
- Наибольший вклад в покрытие внесли тесты бизнес-логики и интеграции со Stripe.

### 5. Выводы о качестве тестирования и обнаруженных проблемах

**Качество тестирования:**

Тесты покрывают критические сценарии, включая взаимодействие логики с БД, корректную обработку данных заказа, а также успешные и аварийные сценарии при обращении к Stripe API

В результате интеграционные ошибки обнаруживаются на раннем этапе, а корректность работы ключевых частей приложения подтверждена

**Обнаруженные проблемы:**

- Зависимость от внешнего сервиса	Без моков приложение не может стабильно тестироваться;
- Отсутствие проверки для пустых заказов	Добавление теста улучшит устойчивость логики.



