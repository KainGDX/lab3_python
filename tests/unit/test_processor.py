import pytest

# ПРИМЕЧАНИЕ: Замени пути импортов на те, что используются в твоем проекте
from app.services.processor import validate_record
from app.core.exceptions import ValidationError, InvalidTransactionError

# --- ТЕСТ 1: Валидация с параметризацией (10+ случаев) ---
@pytest.mark.parametrize("amount, should_pass", [
    (0.01, True),          # Минимально возможное положительное (Граничное)
    (100.0, True),         # Обычное значение
    (999999999.99, True),  # Очень большое число
    (0, False),            # Ноль (Ошибка)
    (-0.01, False),        # Отрицательное (Граничное)
    (-1000, False),        # Отрицательное большое
    ("abc", False),        # Строка вместо числа
    (None, False),         # Пустое значение
    ([], False),           # Неверный тип данных
    ({}, False)            # Неверный тип данных
])
def test_validate_record_amount(valid_transaction, amount, should_pass):
    # Arrange
    valid_transaction["amount"] = amount
    
    # Act & Assert
    if should_pass:
        # Если данные верны, функция должна вернуть обработанный словарь
        result = validate_record(valid_transaction)
        assert result["amount"] == float(amount)
    else:
        # Если данные неверны, ждем ошибку ValidationError
        with pytest.raises(ValidationError):
            validate_record(valid_transaction)

# --- ТЕСТ 2: Проверка на обработку полного "мусора" ---
def test_validate_record_garbage_input():
    # Arrange: передаем список вместо словаря
    garbage_data = ["я", "вообще", "не", "транзакция"]
    
    # Act & Assert: программа должна выкинуть кастомную ошибку, а не упасть с TypeError/IndexError
    with pytest.raises(InvalidTransactionError):
        validate_record(garbage_data)