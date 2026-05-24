# Импортируем ОБЕ ошибки из исключений
from app.core.exceptions import ValidationError, InvalidTransactionError

def validate_record(record: dict) -> dict:
    """Проверяет запись. Ожидает ключи: id, amount, category, date, currency"""
    
    # ТРЕБОВАНИЕ ИЗ ТЗ: Проверяем, что пришел именно словарь. 
    # Если пришел мусор (список, строка, число) — кидаем InvalidTransactionError
    if not isinstance(record, dict):
        raise InvalidTransactionError(f"Ожидался словарь (dict), получен {type(record).__name__}")

    required = ['id', 'amount', 'category', 'date', 'currency']

    for key in required:
        if key not in record or not str(record[key]).strip():
            raise ValidationError(f"Отсутствует поле или оно пустое: {key}")

    try:
        amount = float(record['amount'])
        if amount <= 0:
            raise ValidationError(f"Сумма должна быть > 0, получено: {amount}")
    except (ValueError, TypeError):
        raise ValidationError(f"Некорректный формат суммы: {record['amount']}")

    return {
        "id": record['id'],
        "amount": amount,
        "category": record['category'].strip(),
        "currency": record['currency'].strip().upper()
    }