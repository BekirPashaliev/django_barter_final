# Barter – платформа обмена вещами

![Build](https://img.shields.io/badge/build-passing-brightgreen) ![Python](https://img.shields.io/badge/python-3.12-blue)

> **Barter** — это учебный pet‑project, реализующий бартерную систему: пользователи размещают объявления о товарах, ищут подходящие предметы и предлагают обмен. Проект написан в рамках тестового задания компании **Effective Mobile** и демонстрирует базовые навыки Django + DRF.

---

## Содержание

1. [Функциональность](#функциональность)
2. [Стек](#стек)
3. [Установка](#установка)
4. [Запуск](#запуск)
5. [REST API](#rest-api)
6. [Тесты и линтинг](#тесты-и-линтинг)
7. [Docker & CI](#docker--ci)
8. [Roadmap](#roadmap)
9. [Автор и лицензия](#автор-и-лицензия)

---

## Функциональность

* Регистрация (авто-логин) и стандартная аутентификация Django
* **Профиль пользователя** с аватаром `jpg/png` и произвольной биографией  
  (`/accounts/profile/`, `/accounts/profile/edit/`)
* CRUD для объявлений (`Ad`)
* Поиск, фильтр (категория / состояние) и пагинация списка объявлений
* Механизм предложений обмена (`ExchangeProposal`) с тремя статусами: `pending`, `accepted`, `declined`
* Проверка прав: редактировать / удалять объявление может только его автор; статус предложения меняет только владелец объявления‑получателя
* Веб‑интерфейс на Bootstrap 5
* REST API c автодокументацией (Swagger / ReDoc)
* **15 Pytest-тестов** (модели, права, поиск, API, профиль)  
  → `pytest -q  # 15 passed`

## Стек

| Слой               | Технологии                                 |
| ------------------ |--------------------------------------------|
| Язык               | Python 3.12                                |
| Бэкенд             | Django 5.2, Django REST Framework 3.14     |
| БД (по умолчанию)  | SQLite 3 (легко переключить на PostgreSQL) |
| Шаблоны            | Django Templates + Bootstrap 5             |
| Документация API   | drf‑spectacular (OpenAPI 3)                |
| Тесты              | Pytest + pytest‑django                     |
| Статический анализ | Ruff / Black                               |
| CI                 | GitHub Actions                             |
| Контейнеризация    | Docker, docker‑compose                     |

## Установка

```bash
# 1. Склонируйте репозиторий
$ git clone https://github.com/<your_username>/barter-platform.git
$ cd barter-platform

# 2. Создайте виртуальное окружение
$ python -m venv venv && source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Установите зависимости
$ pip install -r requirements.txt

# 4. Примените миграции и создайте суперпользователя
$ python manage.py migrate
$ python manage.py createsuperuser
```

> **Переход на PostgreSQL**: задайте переменную окружения `DATABASE_URL=postgres://user:pass@localhost:5432/barter` или отредактируйте блок `DATABASES` в `barter_project/settings.py`.

## Запуск

```bash
# Локальный сервер
$ python manage.py runserver
# Панель администратора
# http://127.0.0.1:8000/admin/
```

Демо‑пользователь (если загружены фикстуры `demo.json`):

```
login: demo
password: demo
```

## REST API

Авто‑схема OpenAPI доступна по адресу:

* **/api/schema/** — JSON‑схема OpenAPI 3
* **/api/docs/** — Swagger UI

| Endpoint               | Метод(ы)               | Описание                                  |
| ---------------------- | ---------------------- | ----------------------------------------- |
| `/api/ads/`            | GET, POST              | Список объявлений / создание объявления   |
| `/api/ads/{id}/`       | GET, PUT/PATCH, DELETE | Детали / обновление / удаление объявления |
| `/api/proposals/`      | GET, POST              | Список/создание предложений обмена        |
| `/api/proposals/{id}/` | GET, PUT/PATCH, DELETE | Детали предложения / смена статуса        |

Аутентификация по сессионному cookie (после входа через `/accounts/login/`) или любому совместимому DRF‑токену.

Пример запроса:

```bash
curl -X POST http://127.0.0.1:8000/api/ads/ \
     -H "Content-Type: application/json" \
     -d '{"title":"Книга Dune", "description":"Новая, в плёнке", "category":"Books", "condition":"new"}' \
     -u demo:demo
```

## Тесты и линтинг

```bash
# Запуск Pytest
$ pytest --cov=ads

# Проверка стиля
$ ruff check . && ruff format .
```

## Docker & CI

```bash
# Поднять всё в контейнерах (Django + PostgreSQL)
$ docker compose up --build
```

CI‑workflow (`.github/workflows/ci.yml`) автоматически запускает тесты и линтинг при push / PR.

## Roadmap

* [ ] JWT‑аутентификация
* [ ] Функция «избранное» для объявлений
* [ ] E‑mail / Telegram‑уведомления о новых предложениях
* [ ] React / Next.js фронт на отдельном репозитории

## Автор

Создал **Пашалиев Бекир**, 2025 г.
