import pytest
from unittest.mock import patch, mock_open
from main import main
import json

# --- ТЕСТ 1: ИНТЕГРАЦИЯ (Проверка полной логики с файлами) ---

def test_full_integration_with_files(tmp_path, monkeypatch):
    # Создаем папку data внутри временной папки
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    
    # Создаем CSV файл со ВСЕМИ полями, которые требует твой валидатор (включая date)
    csv_file = data_dir / "test_data.csv"
    csv_file.write_text(
        "id,amount,category,currency,date\n"
        "1,100,Food,USD,2026-05-11\n"
        "2,-50,Error,USD,2026-05-11", 
        encoding='utf-8'
    )

    # Заставляем программу работать во временной папке
    monkeypatch.chdir(tmp_path)

    # Запускаем main()
    main()

    # Проверяем результат
    result_file = tmp_path / "result.json"
    assert result_file.exists(), "Файл result.json не создался"
    
    with open(result_file, 'r', encoding='utf-8') as f:
        output = json.load(f)
        
    # Проверяем, что сумма по Food посчиталась (100.0)
    assert "Food" in output["results"], f"Ключ Food отсутствует в {output['results']}"
    assert output["results"]["Food"] == 100.0


# --- ТЕСТ 2: MOCKING (Проверка обработки ошибки диска) ---

def test_save_results_disk_error_handling(tmp_path, monkeypatch, capsys):
    # Подготовка среды
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    (data_dir / "empty.json").write_text("[]", encoding='utf-8')
    monkeypatch.chdir(tmp_path)

    # Мокаем open, чтобы при записи ('w') вылетала ошибка
    with patch("builtins.open", mock_open()) as m:
        def side_effect(path, mode='r', **kwargs):
            if 'w' in mode:
                raise OSError("Disk write protected")
            # Для чтения возвращаем пустой список
            return mock_open(read_data="[]").return_value

        m.side_effect = side_effect
        
        # Запускаем программу
        main()

    # Захватываем то, что программа напечатала в консоль (stdout)
    captured = capsys.readouterr()
    
    # Проверяем, что твоя строка про ошибку записи появилась на экране
    assert "Ошибка записи результата" in captured.out