class BaseAppError(Exception):
    """Базовое исключение для всего проекта."""
    pass


class DataFormatError(BaseAppError):
    """Выбрасывается, если файл сломан или имеет неверный формат."""
    pass


class ValidationError(BaseAppError):
    """Выбрасывается, если данные нарушают бизнес-логику."""
    pass


class InvalidTransactionError(Exception):
    """Выбрасывается, если вместо транзакции пришел полный мусор (не словарь)."""
    pass


class CurrencyMismatchError(BaseAppError):
    """Ошибка, если в отчетах смешаны разные валюты."""
    pass
