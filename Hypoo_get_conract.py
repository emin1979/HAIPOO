# --- Скрипт Получения Контактов Hypoo ---

# 1. Импорт необходимых библиотек
# 'build' из googleapiclient.discovery позволяет создать сервис для работы с API
# 'HttpError' для обработки ошибок HTTP-запросов
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import json
import os
# Предполагаем, что creds (учетные данные) уже получены из load_hypoo_system()
from google.oauth2.credentials import Credentials

# Файл, где хранится токен, полученный на этапе загрузки
TOKEN_FILE = 'token.json'

def get_google_contacts():
    """
    Функция для получения контактов из Google People API.
    """
    creds = None
    if os.path.exists(TOKEN_FILE):
        try:
            # Загружаем учетные данные из файла
            creds = Credentials.from_authorized_user_file(TOKEN_FILE,
                                                           scopes=['https://www.googleapis.com/auth/contacts.readonly',
                                                                   'https://www.googleapis.com/auth/userinfo.profile'])
        except Exception as e:
            print(f"Hypoo: Ошибка загрузки или чтения токена: {e}")
            return None
    else:
        print("Hypoo: Токен авторизации не найден. Пожалуйста, сначала запустите начальный скрипт загрузки.")
        return None

    if not creds or not creds.valid:
        print("Hypoo: Недействительные учетные данные. Возможно, требуется повторная авторизация.")
        # В реальной системе здесь должна быть логика для повторной авторизации или запроса запуска load_hypoo_system()
        return None

    try:
        # Создаем сервис для работы с People API (версия v1)
        # 'resourceName=people/me' указывает, что мы хотим получить контакты текущего пользователя
        # 'personFields' определяет, какие поля мы хотим получить для каждого контакта
        service = build('people', 'v1', credentials=creds)

        print("Hypoo: Запрос контактов из Google People API...")

        # Выполняем запрос на получение списка контактов
        # 'readGroup=myContacts' фильтрует контакты только из группы "Мои контакты"
        # 'pageSize' определяет количество контактов на одной странице (максимум 1000)
        # 'requestMask.includeField' позволяет запрашивать данные только для указанных полей (для оптимизации)
        results = service.people().connections().list(
            resourceName='people/me',
            pageSize=1000, # Максимальное количество контактов за один запрос
            personFields='names,emailAddresses,phoneNumbers,photos,userDefined,memberships,metadata',
            sortOrder='ALPHABETICAL_ASCENDING' # Сортировка по алфавиту
            # readGroup='myContacts' # Можно использовать для фильтрации по группе "Мои контакты"
        ).execute()

        connections = results.get('connections', [])
        contact_list = []

        if not connections:
            print("Hypoo: Контакты не найдены в вашей учетной записи Google.")
            return []
        else:
            print(f"Hypoo: Найдено {len(connections)} контактов. Обработка...")
            for person in connections:
                # Извлекаем нужные поля
                name = person.get('names', [{}])[0].get('displayName', 'Без имени')
                emails = [e.get('value') for e in person.get('emailAddresses', []) if e.get('value')]
                phones = [p.get('value') for p in person.get('phoneNumbers', []) if p.get('value')]
                user_id = person.get('metadata', {}).get('sources', [{}])[0].get('id') # User ID
                
                # Здесь можно добавить логику для извлечения других полей, например, групп (memberships)
                # memberships = [m.get('contactGroupMembership', {}).get('contactGroupResourceName') for m in person.get('memberships', []) if m.get('contactGroupMembership')]
                
                contact_info = {
                    'name': name,
                    'emails': emails,
                    'phones': phones,
                    'user_id': user_id, # Важный для нас User ID
                    # 'groups': memberships # Можно добавить, если нужно
                    'raw_data': person # Можно сохранить сырые данные для полного анализа
                }
                contact_list.append(contact_info)
                # print(f"  Обработан контакт: {name} ({user_id})") # Для отладки

            print("Hypoo: Контакты успешно получены и обработаны для первичного анализа.")
            return contact_list

    except HttpError as err:
        print(f"Hypoo: Произошла ошибка при доступе к Google API: {err}")
        if err.resp.status == 401:
            print("Hypoo: Ошибка авторизации (401 Unauthorized). Токен недействителен или требует обновления.")
        elif err.resp.status == 403:
            print("Hypoo: Ошибка доступа (403 Forbidden). Проверьте разрешения API.")
        return None
    except Exception as e:
        print(f"Hypoo: Произошла непредвиденная ошибка: {e}")
        return None

if __name__ == '__main__':
    # Эта часть будет запускаться для тестирования скрипта напрямую
    # В реальной системе get_google_contacts() будет вызываться после успешной загрузки Hypoo
    print("--- Тестовый запуск скрипта получения контактов ---")
    contacts = get_google_contacts()
    if contacts:
        print(f"\nHypoo: Получено и готово к дальнейшей обработке {len(contacts)} контактов.")
        # Пример вывода первых 5 контактов для проверки
        # for i, contact in enumerate(contacts[:5]):
        #     print(f"Контакт {i+1}:")
        #     print(f"  Имя: {contact['name']}")
        #     print(f"  Email: {contact['emails']}")
        #     print(f"  Телефон: {contact['phones']}")
        #     print(f"  User ID: {contact['user_id']}")
        #     print("---")
    else:
        print("Hypoo: Не удалось получить контакты.")

