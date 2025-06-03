# Описание проекта

Проект написан на FastAPI + SQLalchemy + Pydantic + SQLite

Выбор SQLite оправдан быстрым стартом и не привязан к наличию сервера СУБД на компьютере пользователя или Docker на компьютере пользователя

Также реализована базовая аутентификация(пароли хэшируются и хранятся в таком виде)

### Возможные улучшения

Если бы обязательным условием выполнения задания было использование PostgreSQL или MySQL, использовал бы docker compose

## Установка и запуск

1. Клонируйте репозиторий:
```bash
git clone https://github.com/Artfal11/url_alias_service.git
cd url_alias_service
```

2. Создайте виртуальное окружение:
```bash
make venv   
```

3. Активируйте виртуальное окружение:
```bash
source venv/bin/activate # Linux/MacOS
# или
venv\Scripts\activate # Windows    
```

4. Установите зависимости
```bash
make install
```


5. Запустите сервер
```bash
make run
```

6. Открывайте ссылку localhost:8000/docs