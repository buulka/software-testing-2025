Университет: **ITMO University**

Факультет: **FICT**

Курс: **Software Testing**

Год: **2025/2026**

Группа: **K3323**

Автор: **Ivanova Ekaterina Andreevna**

Ссылка на репозиторий: **https://github.com/buulka/software-testing-2025/tree/main/lab1**

---

## Лабораторная работа 1. Unit tests

### 1. Описание проекта

**Проект**: 

Программа для преобразования таблицы истинности булевой функции в полином Жегалкина

**Основной функционал**:

- Ввод таблицы истинности булевой функции

- Построение треугольника Паскаля для вычисления коэффициентов

- Формирование полинома Жегалкина

- Визуализация результатов в виде таблицы и треугольника

**Технические особенности**: 

Использует XOR преобразования для вычисления коэффициентов полинома через треугольник Паскаля

### 2. Тестируемые функциональности

- row_xor() - базовое XOR преобразование, основа алгоритма
- make_triangle() - ключевой этап вычислений
- make_polynomial()	- формирование итогового полинома
- граничные случаи - беспечение стабильности при нестандартных входных данных


### 3. Примеры написанных тестов
1. Базовое XOR преобразование
```python
def test_row_xor_basic(self):
    """Тест базового XOR преобразования строки"""
    # Arrange
    test_row = [1, 0, 1, 0]
    expected = [1, 1, 1] 
    
    # Act
    result = row_xor(test_row)
    
    # Assert
    self.assertEqual(result, expected)
```

2. Граничный случай  - строка с одним элементом

```python
def test_row_xor_single_element(self):
    """Тест граничного случая - строка с одним элементом"""
    # Arrange
    test_row = [1]
    expected = [] 
    
    # Act
    result = row_xor(test_row)
    
    # Assert
    self.assertEqual(result, expected)
```

4. Обработка пустой таблицы
```python
def test_make_triangle_empty(self):
    """Тест граничного случая - пустая таблица"""
    # Arrange
    table = []
    n = 0
    
    # Act
    result = make_triangle(table, n)
    
    # Assert
    self.assertEqual(result, [])
```

5. Визуализация треугольника
```python
@patch('sys.stdout', new_callable=StringIO)
def test_draw_triangle(self, mock_stdout):
    """Тест отрисовки треугольника"""
    # Arrange
    triangle = [
        [0, 1, 1, 0],
        [1, 0, 1],
        [1, 1],
        [0]
    ]

    # Act
    draw_triangle(triangle)
    output = mock_stdout.getvalue()

    # Assert
    self.assertTrue(len(output) > 0)
    self.assertIn("  ", output)
```

### 4. Результаты запуска тестов и метрика code coverage

```commandline
test_draw_triangle (test_zhegalkin.TestZhegalkin)
Тест отрисовки треугольника ... ok
test_make_polynomial_2_variables (test_zhegalkin.TestZhegalkin)
Тест формирования полинома для 2 переменных ... ok
test_make_triangle_2_variables (test_zhegalkin.TestZhegalkin)
Тест построения треугольника для 2 переменных ... ok
test_make_triangle_empty (test_zhegalkin.TestZhegalkin)
Тест граничного случая - пустая таблица ... ok
test_make_triangle_single_row (test_zhegalkin.TestZhegalkin)
Тест с одной строкой ... ok
test_row_xor_basic (test_zhegalkin.TestZhegalkin)
Тест базового XOR преобразования строки ... ok
test_row_xor_single_element (test_zhegalkin.TestZhegalkin)
Тест граничного случая - строка с одним элементом ... ok

----------------------------------------------------------------------
Ran 7 tests in 0.000s

OK
```

```commandline
Name                Stmts   Miss  Cover   Missing
-------------------------------------------------
test_zhegalkin.py      50      1    98%   129
zhegalkin.py           56     17    70%   5-12, 66-81, 85
-------------------------------------------------
TOTAL                 106     18    83%
```

### 5. Выводы о качестве тестирования и обнаруженных проблемах

**Качество тестирования:**

- Высокое покрытие: 70% основного кода, 98% общего
- Соблюдены принципы FIRST
- Тесты следуют принципу Arrange-Act-Assert
- Разнообразие тестов: базовые и граничные случаи

**Обнаруженные проблемы:**

1. Функция make_triangle возвращала [[]] для пустой таблицы
    - Добавлена валидация входных данных
   
2. Недостаточное тестирование функции make_polynomial 
   - Добавлены тесты для различных конфигураций полиномов

3. Сложность тестирования функций ввода/вывода
   - Использовано мокирование для draw_triangle

