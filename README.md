# api_yamdb

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

Если необходимо заполнить БД данными з файлов csv:

* Если у вас Linux/macOS:

    ```
    python3 manage.py load_reviews_data.py
    ```

* Если у вас windows:

    ```
    python manage.py load_reviews_data.py
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

