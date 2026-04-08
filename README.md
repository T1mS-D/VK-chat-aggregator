# VK-chat-aggregator

## Что делает проект
- Сохраняет входящие комментарии и записи сообщества в PostgreSQL
- Проверяет каждый комментарий и запись на соответствие промптам подписчиков через LLM
- Отправляет уведомление в личку пользователю при совпадении

## Команды бота
Бот управляется кнопками:
- Создать подписку - `➕ Подписаться` → затем написать тему
- Мои подписки - `📋 Мои подписки`
- Удалить подписку - `🗑 Удалить подписку` → написать `#ID подписки`

## .env — переменные окружения
### Токен сообщества VK
```env
VK_GROUP_TOKEN=ВАШ_ТОКЕН
```
### ID сообщества
```env
VK_GROUP_ID=123456789
```
### OpenRouter (Или аналог)
```env
OPENROUTER_API_KEY=sk-or-v1-xxx
OPENROUTER_MODEL=openai/gpt-oss-120b:free
```
### PostgreSQL
```env
DATABASE_URL=postgresql+asyncpg://postgres:пароль@localhost:5432/vk_aggregator
```

## Быстрый старт
### 1. Клонировать
```bash
git clone https://github.com/T1mS-D/VK-chat-aggregator.git
cd VK-chat-aggregator
```
### 2. Виртуальное окружение
```bash
python3 -m venv venv
source venv/bin/activate
```
### 3. Зависимости
```bash
pip install -r requirements.txt
```
### 4. База данных
```bash
psql -U postgres -c "CREATE DATABASE vk_aggregator;"
```
### 5. Заполнить .env

### 6. Запуск
```bash
python -m app.main
```