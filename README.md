# 📚 Корпоративная Wiki-платформа

> Централизованная система знаний для обучения и работы персонала.  
> Пишите статьи в Markdown, организуйте их по категориям, модерируйте контент и находите нужную информацию за секунды.

![Django](https://img.shields.io/badge/Django-5.0+-092E20?logo=django)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-336791?logo=postgresql)
![HTMX](https://img.shields.io/badge/HTMX-1.9+-000000?logo=htmx)
![Markdown](https://img.shields.io/badge/Markdown-CommonMark-000000?logo=markdown)
![License](https://img.shields.io/badge/License-MIT-blue)

---

## 🎯 Возможности

- ✍️ Создание и редактирование статей в **Markdown**
- 🗂️ Иерархические категории (дерево разделов)
- 🔍 Быстрый поиск по заголовкам и содержимому
- 👥 Роли: пользователь, модератор, администратор
- 📝 Модерация: черновики → на проверку → опубликовано
- ⭐ Закладки и история просмотров
- 📎 Прикрепление файлов (PDF, DOCX, изображения)
- 🖼️ Просмотр изображений в полноэкранном режиме (GLightbox)
- 🔒 Регистрация только по приглашению или через корпоративную почту

---

## 🛠 Технологии

- **Бэкенд**: Django 5.x
- **База данных**: PostgreSQL
- **Фронтенд**: Django Templates + HTMX + Alpine.js (без React!)
- **Редактор**: Чистый Markdown (без WYSIWYG)
- **Поиск**: PostgreSQL Full-Text Search
- **Контейнеризация**: Docker + Docker Compose
- **Тесты**: pytest + factory_boy

> 💡 **Почему без React?**  
> Проект разрабатывается одним человеком. HTMX + Django Templates дают максимальную скорость разработки, SEO и стабильность без сложности SPA.

---

## 🚀 Быстрый старт (локально)

### Требования
- Docker и Docker Compose
- Git

### Установка

```bash
# 1. Клонируйте репозиторий
git clone https://github.com/ваш-логин/corporate-wiki-platform.git
cd corporate-wiki-platform

# 2. Соберите и запустите контейнеры
docker-compose up --build -d

# 3. Примените миграции
docker-compose exec web python manage.py migrate

# 4. Создайте суперпользователя
docker-compose exec web python manage.py createsuperuser

# 5. Откройте в браузере
http://localhost:8000
