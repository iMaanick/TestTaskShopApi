# Документация
Документация api:


```
http://127.0.0.1:8000/docs/
```

# Тесты


```
\tests
```


Запуск тестов:

```
pytest
```

# Запуск проекта

1. Клонируйте репозиторий:

```
git clone https://github.com/iMaanick/TestTaskShopApi.git
```

2. При необходимости установить Poetry ```pip install poetry```

3. Запустить виртуальное окружение ```poetry shell```

4. Установить зависимости ```poetry install```


5. Добавьте файл .env и заполните его как в примере .env.example:

```
DATABASE_URI=DATABASE_URI
```
6. Для запуска выполните:
```
uvicorn --factory app.main:create_app 
```
