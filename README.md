### Спринт 10 - Проект YaMDb (групповой проект). Python-разработчик. Яндекс.Практикум

Команда разработки:
-   [MrSmile1812 (Георгий в роли Тимлида и Python-разработчика)](https://github.com/MrSmile1812)
-   [Puerowe (Никита в роли Python-разработчика)](https://github.com/Puerowe)
-   [Alexandr6400 (Александр в роли Python-разработчика)](https://github.com/Alexandr6400)

### Описание
Проект YaMDb собирает отзывы (Review) пользователей (User) на произведения (Title).
Список категорий (Category) и жанров (Genre) может быть расширен администратором.
Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.

### Стек технологий использованный в проекте:
- Python 3.9
- Django 3.2
- DRF
- JWT

### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/MrSmile1812/api_yamdb
```
```
cd api_yamdb
```

Cоздать, активировать виртуальное окружение и обновить менеджер пакетов:

* Если у вас Linux/macOS:

    ```
    python3 -m venv venv
    source venv/bin/activate
    python3 -m pip install --upgrade pip
    ```

* Если у вас windows:

    ```
    python -m venv venv
    source venv/scripts/activate
    python -m pip install --upgrade pip
    ```


Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Выполнить миграции:


* Если у вас Linux/macOS:

    ```
    python3 manage.py migrate
    ```

* Если у вас windows:

    ```
    python manage.py migrate
    ```

Если необходимо заполнить БД данными из файлов csv:

* Если у вас Linux/macOS:

    ```
    python3 manage.py load_reviews_data
    ```

* Если у вас windows:

    ```
    python manage.py load_reviews_data
    ```

Запустить проект:


* Если у вас Linux/macOS:

    ```
    python3 manage.py runserver
    ```

* Если у вас windows:

    ```
    python manage.py runserver
    ```

### Примеры работы с API для всех пользователей

Подробная документация доступна по эндпоинту /redoc/

Для неавторизованных пользователей работа с API доступна в режиме чтения.

```
Права доступа: Доступно без токена.
GET /api/v1/categories/ - Получение списка всех категорий
GET /api/v1/genres/ - Получение списка всех жанров
GET /api/v1/titles/ - Получение списка всех произведений
GET /api/v1/titles/{title_id}/reviews/ - Получение списка всех отзывов
GET /api/v1/titles/{title_id}/reviews/{review_id}/comments/ - Получение списка всех комментариев к отзыву
```

### Алгоритм регистрации пользователей
-   Пользователь отправляет POST-запрос на добавление нового пользователя с параметрами email и username на эндпоинт /api/v1/auth/signup/.

```json
{
    "email": "string",
    "username": "string"
}

```

-   YaMDB отправляет письмо с кодом подтверждения (confirmation_code) на адрес email.
-   Пользователь отправляет POST-запрос с параметрами username и confirmation_code на эндпоинт /api/v1/auth/token/, в ответе на запрос ему приходит token (JWT-токен).

```json
{
    "username": "string",
    "confirmation_code": "string"
}
```

-   При желании пользователь отправляет PATCH-запрос на эндпоинт /api/v1/users/me/ и заполняет поля в своём профайле (описание полей — в документации).

```json
{
    "username": "string",
    "email": "user@example.com",
    "first_name": "string",
    "last_name": "string",
    "bio": "string"
}
```

### Пользовательские роли

-   Аноним — может просматривать описания произведений, читать отзывы и комментарии.
-   Аутентифицированный пользователь (user) — может, как и Аноним, читать всё, дополнительно он может публиковать отзывы и ставить оценку произведениям (фильмам/книгам/песенкам), может комментировать чужие отзывы; может редактировать и удалять свои отзывы и комментарии. Эта роль присваивается по умолчанию каждому новому пользователю.
-   Модератор (moderator) — те же права, что и у Аутентифицированного пользователя плюс право удалять любые отзывы и комментарии.
-   Администратор (admin) — полные права на управление всем контентом проекта. Может создавать и удалять произведения, категории и жанры. Может назначать роли пользователям.
-   Суперюзер Django — обладет правами администратора (admin)

### Примеры работы с API для авторизованных пользователей

Добавление категории:

```
Права доступа: Администратор.
POST /api/v1/categories/
```

```json
{
    "name": "string",
    "slug": "string"
}
```

Удаление категории:

```
Права доступа: Администратор.
DELETE /api/v1/categories/{slug}/
```

Добавление жанра:

```
Права доступа: Администратор.
POST /api/v1/genres/
```

```json
{
    "name": "string",
    "slug": "string"
}
```

Удаление жанра:

```
Права доступа: Администратор.
DELETE /api/v1/genres/{slug}/
```

Добавление произведения:

```
Права доступа: Администратор. 
Нельзя добавлять произведения, которые еще не вышли (год выпуска не может быть больше текущего).

POST /api/v1/titles/
```

```json
{
    "name": "string",
    "year": 0,
    "description": "string",
    "genre": [
        "string"
    ],
    "category": "string"
}
```

Получение информации о произведении:

```
Права доступа: Доступно без токена
GET /api/v1/titles/{titles_id}/
```

```json
{
    "id": 0,
    "name": "string",
    "year": 0,
    "rating": 0,
    "description": "string",
    "genre": [
        {
            "name": "string",
            "slug": "string"
        }
    ],
    "category": {
        "name": "string",
        "slug": "string"
    }
}
```

Частичное обновление информации о произведении:

```
Права доступа: Администратор
PATCH /api/v1/titles/{titles_id}/
```

```json
{
    "name": "string",
    "year": 0,
    "description": "string",
    "genre": [
        "string"
    ],
    "category": "string"
}
```

Удаление произведения:
```
Права доступа: Администратор
DEL /api/v1/titles/{titles_id}/
```

Принцип работы TITLES, REVIEWS и COMMENTS аналогичен, более подробно по эндпоинту /redoc/

### Работа с пользователями:

Для работы с пользователя есть некоторые ограничения.
Получение списка всех пользователей.

```
Права доступа: Администратор
GET /api/v1/users/ - Получение списка всех пользователей
```

Добавление пользователя:

```
Права доступа: Администратор
Поля email и username должны быть уникальными.
POST /api/v1/users/ - Добавление пользователя
```

```json
{
    "username": "string",
    "email": "user@example.com",
    "first_name": "string",
    "last_name": "string",
    "bio": "string",
    "role": "user"
}
```

Получение пользователя по username:

```
Права доступа: Администратор
GET /api/v1/users/{username}/ - Получение пользователя по username
```

Изменение данных пользователя по username:

```
Права доступа: Администратор
PATCH /api/v1/users/{username}/ - Изменение данных пользователя по username
```

```json
{
    "username": "string",
    "email": "user@example.com",
    "first_name": "string",
    "last_name": "string",
    "bio": "string",
    "role": "user"
}
```

Удаление пользователя по username:

```
Права доступа: Администратор
DELETE /api/v1/users/{username}/ - Удаление пользователя по username
```

Получение данных своей учетной записи:

```
Права доступа: Любой авторизованный пользователь
GET /api/v1/users/me/ - Получение данных своей учетной записи
```

Изменение данных своей учетной записи:

- Права доступа: Любой авторизованный пользователь
```
PATCH /api/v1/users/me/ # Изменение данных своей учетной записи
```

```json
{
    "username": "string",
    "email": "user@example.com",
    "first_name": "string",
    "last_name": "string",
    "bio": "string"
}
```

Проект сделан в рамках учебного процесса по специализации Python-разработчик (back-end) Яндекс.Практикум.
