# Barter Platform

Skeleton Django project for the barter exchange test assignment.

## Quick start

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```


## REST API (DRF)
| Endpoint | Метод | Описание |
|----------|-------|----------|
| `/api/ads/` | GET/POST | Список объявлений / создание |
| `/api/ads/{id}/` | GET/PUT/PATCH/DELETE | CRUD для объявления |
| `/api/proposals/` | GET/POST | Просмотр/создание предложений|
| `/api/proposals/{id}/` | GET/PUT/PATCH/DELETE | Детали/обновление статуса |

## Тесты
```bash
pytest
```
