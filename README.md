# Meetups

[![Django CI](https://github.com/Vladislove11/meetups_site/actions/workflows/django.yml/badge.svg)](https://github.com/Vladislove11/meetups_site/actions/workflows/django.yml)

Учебный проект — сайт для организации митапов.

## Возможности

- Список митапов с поиском
- Детальная страница митапа
- Регистрация на митап (только для залогиненных)
- Отмена регистрации
- Редактирование митапа (только автор)
- Русский интерфейс
- Админка с настройками

## Стек

- Python 3.10+
- Django 4.2
- SQLite
- HTML / CSS

## Установка

```bash
git clone https://github.com/Vladislove11/meetups_site.git
cd meetups_site
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver