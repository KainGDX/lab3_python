import json
import csv
from pathlib import Path
from app.core.exceptions import DataFormatError


def read_json(path: Path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        raise DataFormatError(f"Ошибка чтения JSON: {e}")


def read_csv(path: Path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return list(csv.DictReader(f))
    except Exception as e:
        raise DataFormatError(f"Ошибка чтения CSV: {e}")


# Registry Pattern: связываем расширение с функцией
HANDLERS = {
    '.json': read_json,
    '.csv': read_csv
}
