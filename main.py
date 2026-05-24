import logging
import json
import sys
from pathlib import Path

from app.core.exceptions import BaseAppError, CurrencyMismatchError
from app.io.readers import HANDLERS
from app.services.processor import validate_record

# Настройка логирования
logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    encoding='utf-8'
)


def main():
    data_dir = Path('data')
    if not data_dir.exists():
        logging.critical("Директория 'data' не найдена!")
        print("Ошибка: Создайте папку 'data'.")
        sys.exit(1)

    aggregated_data = {}
    processed_ids = set()
    base_currency = None

    stats = {"total": 0, "success": 0, "errors": 0}
    error_details = []

    for file_path in data_dir.iterdir():
        if not file_path.is_file():
            continue

        stats["total"] += 1
        ext = file_path.suffix.lower()

        try:
            if ext not in HANDLERS:
                raise BaseAppError(f"Формат {ext} не поддерживается")

            # 1. Читаем файл
            records = HANDLERS[ext](file_path)
            if isinstance(records, dict):
                records = [records]

            # 2. Обрабатываем записи
            for raw_item in records:
                item = validate_record(raw_item)

                # Проверка валюты (CurrencyMismatchError)
                if base_currency is None:
                    base_currency = item['currency']
                elif item['currency'] != base_currency:
                    raise CurrencyMismatchError(
                        f"Конфликт: {item['currency']} вместо {base_currency}"
                    )

                # Проверка дубликатов (Data Integrity)
                if item['id'] in processed_ids:
                    logging.warning(
                        f"Дубликат ID {item['id']} в {file_path.name} Пропущен"
                    )
                    continue

                processed_ids.add(item['id'])
                cat = item['category']
                aggregated_data[cat] = (
                    aggregated_data.get(cat, 0.0) + item['amount']
                )

            stats["success"] += 1
            logging.info(f"Файл {file_path.name} успешно обработан.")

        except BaseAppError as e:
            stats["errors"] += 1
            msg = f"Ошибка в {file_path.name}: {e}"
            error_details.append(msg)
            logging.error(msg)
        except Exception as e:
            stats["errors"] += 1
            logging.error(f"Критический сбой файла {file_path.name}: {e}")

    # Итоговый экспорт (Транзакционная запись)
    output = {
        "metadata": {
            "currency": base_currency,
            "files_processed": stats["total"],
            "successful_files": stats["success"]
        },
        "results": aggregated_data
    }

    tmp_file = Path("result.json.tmp")
    final_file = Path("result.json")

    try:
        with open(tmp_file, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=4, ensure_ascii=False)
        tmp_file.replace(final_file)
        print(
            f"\nОбработано: {stats['total']}"
            f"\nУспешно: {stats['success']}"
            f"\nОшибок: {stats['errors']}"
        )
        print("Результат в result.json, детали ошибок в app.log")
    except Exception as e:
        print(f"Ошибка записи результата: {e}")


if __name__ == "__main__":
    main()
