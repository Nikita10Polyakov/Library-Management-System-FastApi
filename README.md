# Library-Management-System-FastApi

Library Management System – це RESTful API, створене на FastAPI, яке дозволяє керувати книгами, авторами, жанрами, позиками та видавцями у бібліотечній системі.
<br><br>

# Запуск проєкту

## 1) Клонувати репозиторій:

git clone https://github.com/Nikita10Polyakov/Library-Management-System-FastApi.git

cd Library-Management-System-FastApi

## 2) Встановити залежності:

pip install -r requirements.txt

## 3) Запустити сервер:

uvicorn main:app --reload

## 4) Документація API:

Swagger UI: http://127.0.0.1:8000/docs
<br><br>

# Опис ендпоінтів

## 1) Книги:

GET /books – Отримати список книг (з пагінацією та сортуванням).

POST /books – Додати нову книгу (перевірка ISBN, дата в минулому).

GET /books/{id}/history – Отримати історію позик книги.

## 2) Автори:

GET /authors/{id}/books – Отримати всі книги автора.

POST /authors – Додати автора (унікальне ім'я, дата народження в минулому).

## 3) Позики:

POST /borrow – Позичити книгу (не більше 5 книг на користувача).

POST /return – Повернути книгу (перевірка, що її позичив цей користувач).

## 4) Жанри:

GET /genres – Отримати всі жанри.

POST /genres – Додати новий жанр (унікальність).

## 5) Видавці:

GET /publishers – Отримати всіх видавців.

POST /publishers – Додати видавця (унікальне ім'я, рік не в майбутньому).
<br><br>

# Валідація даних (Pydantic)

ISBN → Перевіряється через регулярний вираз.

Дата народження автора → Не може бути в майбутньому.

Дата публікації книги → Не може бути в майбутньому.

Рік заснування видавця → Не може бути у майбутньому.


## Автор

Микита

GitHub: @Nikita10Polyakov
