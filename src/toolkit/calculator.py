from toolkit.errors import ToolkitError


def tokenize(expression: str) -> list:
    """Шаг 1. Разбивает строку на числа (float) и операторы.

    Алгоритм полностью игнорирует пробелы между токенами и выбрасывает
    ToolkitError, если встречает недопустимые символы (например, буквы).
    """
    # Проверяем обязательное требование: пустое выражение или только пробелы
    if not expression.strip():
        raise ToolkitError("Empty expression")

    tokens = []
    current_number = ""  # Временный буфер, куда мы посимвольно копим число

    i = 0
    while i < len(expression):
        char = expression[i]

        # Если символ — пробел, просто пропускаем его согласно критериям
        if char.isspace():
            i += 1
            continue

        # Если символ — цифра или точка, добавляем её в буфер числа
        if char.isdigit() or char == ".":
            current_number += char
        else:
            # Если мы дошли до оператора, но в буфере скопилось число —
            # сначала переводим его во float и сохраняем в итоговый список
            if current_number:
                try:
                    tokens.append(float(current_number))
                except ValueError:
                    raise ToolkitError("Invalid numeric value")
                current_number = ""  # Очищаем буфер для следующего числа

            # Проверяем, является ли символ допустимым бинарным оператором
            if char in ("+", "-", "*", "/"):
                tokens.append(char)
            else:
                # Обязательная проверка на недопустимый символ (например, "2+a")
                raise ToolkitError(f"Invalid character: '{char}'")
        i += 1

    # Если строка закончилась, но в буфере осталось последнее число — добавляем его
    if current_number:
        try:
            tokens.append(float(current_number))
        except ValueError:
            raise ToolkitError("Invalid numeric value")

    return tokens


def validate_and_process_unaries(tokens: list) -> list:
    """Шаг 2. Валидирует токены и обрабатывает унарные знаки.

    Склеивает унарные '+' и '-' с числами. Выбрасывает ToolkitError, если
    обнаруживает синтаксические ошибки (например, два бинарных оператора подряд).
    """
    if not tokens:
        raise ToolkitError("Empty expression")

    processed_tokens = []
    i = 0
    n = len(tokens)

    while i < n:
        token = tokens[i]

        # Как алгоритм понимает, что знак унарный?
        # Знак унарный, если он стоит в самом начале (i == 0)
        # ИЛИ если он стоит сразу после другого оператора (последний элемент в processed_tokens — строка)
        if token in ("+", "-") and (i == 0 or isinstance(processed_tokens[-1], str)):
            # Ошибка: унарный знак стоит в самом конце выражения (например, "2 + -")
            if i + 1 >= n:
                raise ToolkitError("Missing operand")

            next_token = tokens[i + 1]

            # Если за унарным знаком идет число — склеиваем их в одно отрицательное/положительное число
            if isinstance(next_token, float):
                value = next_token if token == "+" else -next_token
                processed_tokens.append(value)
                i += 2  # Перешагиваем через обработанное число
                continue
            else:
                # Ошибка: два бинарных оператора подряд (например, "2 * - + 3")
                raise ToolkitError("Two binary operators in a row")

        # Обязательная проверка на два бинарных оператора подряд (например, "2 * / 3")
        if isinstance(token, str) and i > 0 and isinstance(processed_tokens[-1], str):
            raise ToolkitError("Two binary operators in a row")

        processed_tokens.append(token)
        i += 1

    # Проверка: выражение не может заканчиваться оператором (например, "2 +")
    if processed_tokens and isinstance(processed_tokens[-1], str):
        raise ToolkitError("Missing operand")

    return processed_tokens


def _execute_ops(tokens: list, target_operators: tuple) -> list:
    """Вспомогательная функция для прохода по токенам и выполнения операций.

    Выполняет бинарные операции из переданного кортежа target_operators
    строго слева направо.
    """
    i = 0
    while i < len(tokens):
        if tokens[i] in target_operators:
            op = tokens[i]
            left_operand = tokens[i - 1]
            right_operand = tokens[i + 1]

            # Выполняем базовые математические действия
            if op == "*":
                result = left_operand * right_operand
            elif op == "/":
                # Обязательное требование преподавателя: обработка деления на ноль
                if right_operand == 0:
                    raise ToolkitError("Division by zero")
                result = left_operand / right_operand
            elif op == "+":
                result = left_operand + right_operand
            elif op == "-":
                result = left_operand - right_operand

            # Схлопываем список: заменяем три элемента (число, знак, число) на результат
            tokens[i - 1 : i + 2] = [result]
            # Индекс i не увеличиваем, так как длина списка уменьшилась
            continue
        i += 1
    return tokens


def calculate(expression: str):
    """Главная функция вычислительного ядра калькулятора.

    Связывает воедино токенизацию, валидацию и расчет по приоритетам.
    """
    # Фаза 1. Токенизация (разбиение строки на числа и знаки)
    raw_tokens = tokenize(expression)

    # Фаза 2. Валидация и обработка унарных знаков
    clean_tokens = validate_and_process_unaries(raw_tokens)

    # Фаза 3. Вычисление: сначала Проход А (умножение и деление как приоритетные)
    clean_tokens = _execute_ops(clean_tokens, ("*", "/"))

    # Фаза 3. Вычисление: Проход Б (оставшиеся сложение и вычитание)
    clean_tokens = _execute_ops(clean_tokens, ("+", "-"))

    # Валидация структуры: в конце в списке должен остаться ровно один элемент
    if len(clean_tokens) != 1 or isinstance(clean_tokens[0], str):
        raise ToolkitError("Invalid expression structure")

    result = clean_tokens[0]

    # Если результат вещественный, но число целое (например, 5.0) —
    # приводим к int для красивого вывода, иначе возвращаем float
    return int(result) if result.is_integer() else result
