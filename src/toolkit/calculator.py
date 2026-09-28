from toolkit.errors import ToolkitError


def tokenize(expression: str) -> list:
    """Разбивает строку на числа (float) и операторы, игнорируя пробелы."""
    if not expression.strip():
        raise ToolkitError("пустое выражение")

    tokens = []
    current_number = ""

    i = 0
    while i < len(expression):
        char = expression[i]

        if char.isspace():
            i += 1
            continue

        if char.isdigit() or char == ".":
            current_number += char
        else:
            if current_number:
                try:
                    tokens.append(float(current_number))
                except ValueError:
                    raise ToolkitError("неверное числовое значение")
                current_number = ""

            if char in ("+", "-", "*", "/"):
                tokens.append(char)
            else:
                raise ToolkitError("недопустимый символ")
        i += 1

    if current_number:
        try:
            tokens.append(float(current_number))
        except ValueError:
            raise ToolkitError("неверное числовое значение")

    return tokens


def validate(tokens: list) -> list:
    """Проверяет синтаксические ошибки и обрабатывает унарные знаки."""
    if not tokens:
        raise ToolkitError("пустое выражение")

    if tokens[0] in ("*", "/"):
        raise ToolkitError("пропущенный операнд")

    processed_tokens = []
    i = 0
    n = len(tokens)

    while i < n:
        token = tokens[i]

        # Проверка на унарный знак перед числом
        if token in ("+", "-") and (i == 0 or isinstance(processed_tokens[-1], str)):
            if i + 1 >= n:
                raise ToolkitError("пропущенный операнд")

            next_token = tokens[i + 1]

            if isinstance(next_token, float):
                value = next_token if token == "+" else -next_token
                processed_tokens.append(value)
                i += 2
                continue
            else:
                raise ToolkitError("два бинарных оператора подряд")

        # Проверка на два бинарных оператора подряд
        if isinstance(token, str) and i > 0 and isinstance(processed_tokens[-1], str):
            raise ToolkitError("два бинарных оператора подряд")

        processed_tokens.append(token)
        i += 1

    if processed_tokens and isinstance(processed_tokens[-1], str):
        raise ToolkitError("пропущенный операнд")

    return processed_tokens


def calculate(expression: str) -> float:
    """Вычисляет результат выражения в два прохода по приоритетам операторов."""
    raw_tokens = tokenize(expression)
    tokens = validate(raw_tokens)

    # Проход А: Выполняем приоритетные операции (*, /) слева направо
    i = 0
    while i < len(tokens):
        if tokens[i] in ("*", "/"):
            op = tokens[i]
            left_operand = tokens[i - 1]
            right_operand = tokens[i + 1]

            if op == "*":
                result = left_operand * right_operand
            elif op == "/":
                if right_operand == 0:
                    raise ToolkitError("деление на ноль")
                result = left_operand / right_operand

            tokens[i - 1 : i + 2] = [result]
            continue
        i += 1

    # Проход Б: Выполняем оставшиеся операции (+, -) слева направо
    i = 0
    while i < len(tokens):
        if tokens[i] in ("+", "-"):
            op = tokens[i]
            left_operand = tokens[i - 1]
            right_operand = tokens[i + 1]

            if op == "+":
                result = left_operand + right_operand
            elif op == "-":
                result = left_operand - right_operand

            tokens[i - 1 : i + 2] = [result]
            continue
        i += 1

    if len(tokens) != 1 or isinstance(tokens[0], str):
        raise ToolkitError("неверное числовое значение")

    return float(tokens[0])
