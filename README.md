# Bank App API

![Python](https://img.shields.io/badge/Python-3.11%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-green)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0+-red)
![Alembic](https://img.shields.io/badge/Alembic-1.12+-orange)
![Uvicorn](https://img.shields.io/badge/Uvicorn-0.25+-brightgreen)
![Pydantic](https://img.shields.io/badge/Pydantic-2.0+-purple)
![AuthX](https://img.shields.io/badge/AuthX-1.0+-blueviolet)
![License](https://img.shields.io/badge/License-MIT-yellow)
![GitHub last commit](https://img.shields.io/github/last-commit/KEgubov/bank-app-api)

**REST API для банковского приложения**, реализованный на **FastAPI** с аутентификацией через **AuthX** (JWT) и хранением данных в **PostgreSQL**.

Этот проект создан для портфолио Junior разработчика. Он демонстрирует навыки разработки бэкенда: работа с аутентификацией, проектирование API, взаимодействие с базой данных.

## 🚀 Возможности

- Регистрация и вход пользователей с получением JWT-токенов (AuthX)
- Защищённые маршруты (требуют валидный токен)
- База данных PostgreSQL с SQLAlchemy (psycopg2)
- Управление переменными окружения (Pydantic Settings)
- Автоматическая интерактивная документация API (Swagger UI)

## 🛠 Технологии

- **FastAPI** – веб-фреймворк
- **AuthX** – аутентификация и JWT
- **PostgreSQL** – реляционная БД
- **SQLAlchemy** – ORM
- **Alembic** – миграции базы данных
- **Pydantic** – валидация данных
- **Uvicorn** – ASGI-сервер

## 📦 Установка и запуск

### Требования

- Python 3.11+
- PostgreSQL 
- Git

## 1. Клонирование репозитория

```bash
git clone https://github.com/KEgubov/bank-app-api.git
cd bank-app-api
```

## 2. Создание виртуального окружения
```bash
python -m venv venv
source venv/bin/activate      # Linux/macOS
venv\Scripts\activate         # Windows
```

## 3. Установка зависимостей
```bash
pip install -r requirements.txt
```

## 4. Настройка переменных окружения
```bash
cp .env.example .env           # Cкопируйте файл-пример и заполните свои значения
```
### Отредактируйте .env (укажите URL вашей БД и секретный ключ):
```ini
DB_HOST=localhost
DB_PORT=5432
DB_USER=postgres
DB_PASS=password
DB_NAME=db_name


JWT_SECRET_KEY=your-secret-key-here-change-me
JWT_ACCESS_COOKIE_NAME=your_jwt_cookie_name
```
## 5. Создание базы данных (локальный PostgreSQL)

### Восстановите схему из дампа:
```bash
psql -U postgres -d bank_app -f schema.sql
```

## 6. Применение миграций (Alembic)
```bash
alembic upgrade head
```

## 7. Запуск сервера (Uvicorn)
```bash
uvicorn app.main:app --reload
```

## 📚 Документация API
**После запуска сервера документация доступна по ссылкe:**

- **Swagger UI**: http://localhost:8000/docs

### Основные эндпоинты

- **POST** - /bank_app/v1/welcome/register - Создание нового пользователя
- **POST** - /bank_app/v1/welcome/login - Вход, получение JWT-токена
- **POST** - /bank_app/v1/accounts/create - Создание счёта (требуется токен)
- **POST** - /bank_app/v1/cards/add - Добавление карты (требуется токен)
- **POST** - /bank_app/v1/contacts/add - Добавление контакта (требуется токен)

### Пример запроса на вход:

```json
{
  "phone_number": "+79999999999",
  "password": "securepassword"
}
```

### Ответ:

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs..."
}
```
## 🗺 Roadmap

```bash
- [ ] Добавить полноценную регистрацию пользователя
- [ ] Написать тесты (pytest) для всех эндпоинтов
- [ ] Подключить кэширование (Redis) для часто запрашиваемых данных
- [ ] Добавить логирование (через `loguru` или стандартный `logging`)
- [ ] Контейнеризация: добавить `Dockerfile` и `docker-compose.yml`
- [ ] Настроить CI/CD (GitHub Actions) для автоматического запуска тестов
- [ ] Создать фронтенд для демонстрации

> **Примечание:** Планы могут меняться, но эти задачи помогут сделать проект ещё надежнее и удобнее.
```

## 💡 Вдохновение

Проект создан под впечатлением от главы о транзакциях из книги **Алана Болье «Изучаем SQL»** (Alan Beaulieu, "Learning SQL").  
Идеи атомарности операций, согласованности данных и работы с финансовыми записями легли в основу проектирования логики счетов и переводов в этом приложении.

## 📄Лицензия

**Проект распространяется под лицензией MIT – подробности в файле LICENSE.**

## 🤝 Вклад в проект
**Это портфолио-проект, но любые замечания и предложения приветствуются. Открывайте Issue или пишите на почту.**

## 📬 Контакты

**Кирилл Егубов**
- **Telegram** – @Maestro2344 
- **Почта** - kirilegubov@gmail.com

Ссылка на проект: https://github.com/KEgubov/bank-app-api