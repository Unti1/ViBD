# Система учета инвентаря спортивного клуба

## Описание
Система для управления инвентарем спортивного клуба, включающая функционал для работы с сотрудниками, клиентами, оборудованием, заказами, отзывами, чатами и рабочими сменами.

## Технологии
- Python 3.11
- FastAPI
- SQLAlchemy
- MySQL 8.0
- Alembic
- Poetry

## Установка

1. Клонируйте репозиторий:
```bash
git clone <repository-url>
cd sports-club-inventory
```

2. Установите зависимости с помощью Poetry:
```bash
poetry install
```

3. Создайте файл `.env` в корневой директории проекта со следующим содержимым:
```env
PROJECT_NAME="Sports Club Inventory"
VERSION="1.0.0"
API_V1_STR="/api/v1"

MYSQL_USER=your_mysql_user
MYSQL_PASSWORD=your_mysql_password
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_DB=sports_club

SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

4. Создайте базу данных MySQL:
```sql
CREATE DATABASE sports_club CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

5. Примените миграции:
```bash
alembic upgrade head
```

## Запуск

1. Активируйте виртуальное окружение:
```bash
poetry shell
```

2. Запустите сервер:
```bash
uvicorn app.main:app --reload
```

3. Откройте Swagger UI по адресу: http://localhost:8000/docs

## API Endpoints

### Пользователи
- `GET /api/v1/users/` - Получить список пользователей
- `POST /api/v1/users/` - Создать нового пользователя
- `GET /api/v1/users/me` - Получить текущего пользователя
- `PUT /api/v1/users/me` - Обновить текущего пользователя

### Оборудование
- `GET /api/v1/equipment/` - Получить список оборудования
- `POST /api/v1/equipment/` - Добавить новое оборудование
- `GET /api/v1/equipment/{id}` - Получить информацию об оборудовании
- `PUT /api/v1/equipment/{id}` - Обновить информацию об оборудовании

### Заказы
- `GET /api/v1/orders/` - Получить список заказов
- `POST /api/v1/orders/` - Создать новый заказ
- `GET /api/v1/orders/{id}` - Получить информацию о заказе
- `PUT /api/v1/orders/{id}` - Обновить статус заказа

### Отзывы
- `GET /api/v1/reviews/` - Получить список отзывов
- `POST /api/v1/reviews/` - Создать новый отзыв
- `GET /api/v1/reviews/{id}` - Получить информацию об отзыве

### Чаты
- `GET /api/v1/chat/` - Получить список сообщений
- `POST /api/v1/chat/` - Отправить сообщение
- `GET /api/v1/chat/{id}` - Получить информацию о сообщении

### Рабочие смены
- `GET /api/v1/shifts/` - Получить список смен
- `POST /api/v1/shifts/` - Создать новую смену
- `GET /api/v1/shifts/{id}` - Получить информацию о смене
- `PUT /api/v1/shifts/{id}` - Обновить информацию о смене

## Разработка

### Структура проекта
```
sports-club-inventory/
├── alembic/              # Миграции базы данных
├── app/
│   ├── api/             # API endpoints
│   ├── core/            # Основные настройки
│   ├── db/              # Настройки базы данных
│   ├── models/          # SQLAlchemy модели
│   ├── schemas/         # Pydantic схемы
│   ├── services/        # Бизнес-логика
│   └── utils/           # Утилиты
├── tests/               # Тесты
├── .env                 # Переменные окружения
├── alembic.ini          # Конфигурация Alembic
├── pyproject.toml       # Зависимости проекта
└── README.md           # Документация
```

### Тестирование
```bash
pytest
```

## Лицензия
MIT 