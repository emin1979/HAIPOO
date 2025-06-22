import json

def process_data_for_csharp(json_input_string):
    """
    Эта функция имитирует обработку данных, которые могли бы прийти от C#.
    Она принимает JSON-строку, парсит ее, выполняет простую операцию
    и возвращает результат в виде JSON-строки.
    """
    try:
        # 1. Парсим входящую JSON-строку в Python-словарь
        data = json.loads(json_input_string)
        print(f"Получены данные (Python): {data}")

        # Проверяем, что в данных есть нужные нам ключи
        if 'num1' in data and 'num2' in data:
            num1 = data['num1']
            num2 = data['num2']

            # 3. Выполняем простую операцию (например, сложение)
            result = num1 + num2
            print(f"Вычислено (Python): {num1} + {num2} = {result}")

            # 4. Формируем ответный словарь
            response_data = {
                "status": "success",
                "operation": "addition",
                "input_nums": [num1, num2],
                "result": result
            }
        else:
            response_data = {
                "status": "error",
                "message": "Входящие данные должны содержать 'num1' и 'num2'."
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

    # 4. Возвращаем результат в виде JSON-строки
    return json.dumps(response_data)

# --- Примеры использования функции ---

# Пример 1: Корректный ввод
input_from_csharp_1 = '{"num1": 10, "num2": 25}'
output_to_csharp_1 = process_data_for_csharp(input_from_csharp_1)
print(f"\nОтвет для C# (Python): {output_to_csharp_1}")

# Пример 2: Некорректный JSON
input_from_csharp_2 = '{"num1": 10, "num2": 25,' # Здесь ошибка в JSON
output_to_csharp_2 = process_data_for_csharp(input_from_csharp_2)
print(f"\nОтвет для C# (Python): {output_to_csharp_2}")

# Пример 3: Отсутствие нужных ключей
input_from_csharp_3 = '{"value1": 100, "value2": 50}'
output_to_csharp_3 = process_data_for_csharp(input_from_csharp_3)
print(f"\nОтвет для C# (Python): {output_to_csharp_3}")

