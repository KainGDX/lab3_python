import pytest
import sys
import os

# Гарантируем, что pytest увидит папку app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

@pytest.fixture
def valid_transaction():
    """Фикстура: эталонная правильная транзакция."""
    return {
        "id": "123",
        "amount": 100.50,
        "category": "Food",
        "currency": "USD",
        "date": "2026-05-11"
    }