import json

def process_data_for_csharp(json_input_string):
    """
    Эта функция имитирует обработку данных, которые могли бы прийти от C#.
    Она принимает JSON-строку, парсит ее, выполняет операцию
    и возвращает результат в виде JSON-строки.
    """
    try:
        data = json.loads(json_input_string)
        print(f"Получены данные (Python): {data}")

        # Получаем тип операции, по умолчанию 'add' (сложение)
        operation = data.get('operation', 'add')

        # Обработка числовых операций
        if ('num1' in data and 'num2' in data):
            num1 = data['num1']
            num2 = data['num2']
            result = None
            operation_performed_name = ""

            if operation == 'add':
                result = num1 + num2
                operation_performed_name = "addition"
            elif operation == 'multiply':
                result = num1 * num2
                operation_performed_name = "multiplication"
            elif operation == 'subtract':
                result = num1 - num2
                operation_performed_name = "subtraction"
            elif operation == 'divide':
                if num2 != 0:
                    result = num1 / num2
                    operation_performed_name = "division"
                else:
                    response_data = {
                        "status": "error",
                        "message": "Деление на ноль невозможно."
                    }
                    return json.dumps(response_data)
            else:
                response_data = {
                    "status": "error",
                    "message": f"Неизвестная или неподдерживаемая числовая операция: '{operation}'. Попробуйте 'add', 'multiply', 'subtract', 'divide'."
                }
                return json.dumps(response_data)

            print(f"Вычислено (Python) - {operation_performed_name}: {num1} {operation} {num2} = {result}")

            response_data = {
                "status": "success",
                "operation": operation_performed_name,
                "input_nums": [num1, num2],
                "result": result
            }

        # Обработка строковых операций
        elif operation == 'concatenate' and 'str1' in data and 'str2' in data:
            str1 = data['str1']
            str2 = data['str2']
            result = str1 + str2
            operation_performed_name = "string_concatenation"

            print(f"Вычислено (Python) - {operation_performed_name}: '{str1}' + '{str2}' = '{result}'")

            response_data = {
                "status": "success",
                "operation": operation_performed_name,
                "input_strings": [str1, str2],
                "result": result
            }
        elif operation == 'upper_case' and 'input_string' in data:
            input_str = data['input_string']
            result = input_str.upper()
            operation_performed_name = "to_upper_case"

            print(f"Вычислено (Python) - {operation_performed_name}: '{input_str}' -> '{result}'")

            response_data = {
                "status": "success",
                "operation": operation_performed_name,
                "input_string": input_str,
                "result": result
            }
        elif operation == 'lower_case' and 'input_string' in data:
            input_str = data['input_string']
            result = input_str.lower()
            operation_performed_name = "to_lower_case"

            print(f"Вычислено (Python) - {operation_performed_name}: '{input_str}' -> '{result}'")

            response_data = {
                "status": "success",
                "operation": operation_performed_name,
                "input_string": input_str,
                "result": result
            }
        # Если ни одна из ожидаемых операций не соответствует данным
        else:
            response_data = {
                "status": "error",
                "message": "Недостаточно данных для выполнения запрошенной операции или операция не поддерживается текущими данными. Проверьте 'num1'/'num2' для числовых, 'str1'/'str2'/'input_string' для строковых операций, а также само название 'operation'."
            }

    except json.JSONDecodeError:
        response_data = {
            "status": "error",
            "message": "Некорректный JSON формат входной строки."
        }
    except Exception as e:
        response_data = {
            "status": "error",
            "message": f"Произошла ошибка при обработке: {str(e)}"
        }

    return json.dumps(response_data)

# --- Примеры использования функции с новой логикой ---

print("--- Примеры Числовых Операций ---")
input_add = '{"num1": 10, "num2": 25, "operation": "add"}'
output_add = process_data_for_csharp(input_add)
print(f"\nОтвет для C# (Сложение): {output_add}")

input_multiply = '{"num1": 5, "num2": 8, "operation": "multiply"}'
output_multiply = process_data_for_csharp(input_multiply)
print(f"\nОтвет для C# (Умножение): {output_multiply}")

input_subtract = '{"num1": 100, "num2": 30, "operation": "subtract"}'
output_subtract = process_data_for_csharp(input_subtract)
print(f"\nОтвет для C# (Вычитание): {output_subtract}")

input_divide = '{"num1": 20, "num2": 4, "operation": "divide"}'
output_divide = process_data_for_csharp(input_divide)
print(f"\nОтвет для C# (Деление): {output_divide}")

input_divide_by_zero = '{"num1": 10, "num2": 0, "operation": "divide"}'
output_divide_by_zero = process_data_for_csharp(input_divide_by_zero)
print(f"\nОтвет для C# (Деление на ноль): {output_divide_by_zero}")


print("\n--- Примеры Строковых Операций ---")
input_concat = '{"str1": "Привет, ", "str2": "мир!", "operation": "concatenate"}'
output_concat = process_data_for_csharp(input_concat)
print(f"\nОтвет для C# (Конкатенация): {output_concat}")

input_upper = '{"input_string": "hello python", "operation": "upper_case"}'
output_upper = process_data_for_csharp(input_upper)
print(f"\nОтвет для C# (Верхний регистр): {output_upper}")

input_lower = '{"input_string": "HELLO PYTHON", "operation": "lower_case"}'
output_lower = process_data_for_csharp(input_lower)
print(f"\nОтвет для C# (Нижний регистр): {output_lower}")


print("\n--- Примеры Обработки Ошибок ---")
input_unknown_op = '{"num1": 7, "num2": 3, "operation": "unknown_op"}'
output_unknown_op = process_data_for_csharp(input_unknown_op)
print(f"\nОтвет для C# (Неизвестная операция): {output_unknown_op}")

input_missing_data = '{"num1": 7, "operation": "multiply"}'
output_missing_data = process_data_for_csharp(input_missing_data)
print(f"\nОтвет для C# (Недостаточно данных): {output_missing_data}")

input_incorrect_json = '{"num1": 10, "num2": 25,' # Некорректный JSON
output_incorrect_json = process_data_for_csharp(input_incorrect_json)
print(f"\nОтвет для C# (Некорректный JSON): {output_incorrect_json}")
