Payment Service API
Описание
Сервис для работы с платежами по заказам. Поддерживает наличные и банковские платежи (эквайринг) с синхронизацией статусов через API банка.

Технологии
Python 3.12
FastAPI
PostgreSQL
httpx
Pydantic

Структура
text
BankPaymentSystem/
├── api/               # Работа с БД
├── bank_api/          # Клиент банка
├── config/            # Конфиги
├── sql/               # Схема БД
├── app.py             # FastAPI приложение
├── datamodels.py      # Pydantic модели
├── payment_service.py # Бизнес-логика
└── worker.py          # Фоновый воркер
Установка
bash
git clone <url>
cd BankPaymentSystem

python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
psql -U postgres -f sql/db.sql
cp config/config.example.py config/config.py

Запуск
uvicorn app:app --reload

python worker.py
API Endpoints
Создать платеж
POST /orders/{order_id}/payments?payment_type=cash&amount=1000

Вернуть платеж
POST /payments/{payment_id}/refund?amount=500

Получить заказ
GET /orders/{order_id}
Проверка здоровья
GET /health

Модели данных
Order
id: uuid - ID заказа
amount: int - сумма заказа
status_id: int - статус
customer_id: int - ID покупателя

Payment
id: uuid - ID платежа
order_id: uuid - ID заказа
payment_type_id: int - тип платежа
amount: int - сумма
status_id: int - статус платежа
external_id: str - ID платежа в банке

Статусы
Статусы заказа
1 - unpaid (не оплачен)
2 - partially_paid (частично оплачен)
3 - paid (оплачен)

Статусы платежа
1 - pending (в обработке)
2 - completed (завершен)
3 - cancelled (отменен)
4 - refunded (возвращен)

Типы платежей
1 - cash (наличные)
2 - acquiring (банковская карта)

Интеграция с банком
Эндпоинты банка
POST /acquiring_start - создание платежа

GET /acquiring_check - проверка статуса

Форматы запросов/ответов

CreatePayment
Request: {"order_number": "123", "amount": 1000}
Response: {"payment_id": "bank_123", "status": "pending"}

CheckPayment
Request: {"payment_id": "bank_123"}
Response: {"payment_id": "bank_123", "status": "completed", "amount": 1000, "payment_date": "2024-01-01T12:00:00"}


Конфигурация
# config/config.py

DBHOST = 'localhost'
DBPORT = 5432
DBUSER = 'postgres'
DBPASS = 'postgres'
DBNAME = 'bank_payments'

BANK_API_URL = 'bank.api/'
AQUIRING_START_URL = 'acquiring_start'
AQUIRING_CHECK_URL = 'acquiring_check'

ORDER_STATUS_UNPAID = 'unpaid'
ORDER_STATUS_PARTIALLY_PAID = 'partially_paid'
ORDER_STATUS_PAID = 'paid'

PAYMENT_STATUS_PENDING = 'pending'
PAYMENT_STATUS_COMPLETED = 'completed'
PAYMENT_STATUS_CANCELLED = 'cancelled'
PAYMENT_STATUS_REFUNDED = 'refunded'

PAYMENT_TYPE_CASH = 'cash'
PAYMENT_TYPE_ACQUIRING = 'acquiring'
