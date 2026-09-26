# Toolkit CLI Utilities

Консольный набор утилит, объединяющий калькулятор выражений и конвертер величин.

## Примеры запуска

```bash
# Справка
PYTHONPATH=src python -m toolkit --help

# Калькулятор
PYTHONPATH=src python -m toolkit calc "-2 * -3 + 10 / 4"

# Конвертер
PYTHONPATH=src python -m toolkit convert 1500 --from g --to kg
```

## Тестирование

```bash
python -m pytest
ruff check .
```
