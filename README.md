# WAV to MP3 Telegram Bot

Телеграм-бот, который принимает `.wav` файл и отправляет обратно `.mp3`.
Работает через MTProto (`Pyrogram`), поэтому можно обрабатывать файлы до 50 МБ.
`tgcrypto` не обязателен (без него чуть ниже производительность, но проще деплой).

## Структура (MVC)

- `app/models` — бизнес-логика работы с пользователями.
- `app/repositories` — SQL-слой (PostgreSQL, пользователи, статистика).
- `app/views` — текстовые сообщения и форматирование ответа статистики.
- `app/services` — сервисы бизнес-логики (конвертация WAV -> MP3).
- `bot.py` — точка входа, инициализация и запуск.

## 1) Подготовка

Установи `ffmpeg` (нужен для конвертации):

```bash
brew install ffmpeg
```

Создай и активируй виртуальное окружение:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Установи зависимости:

```bash
pip install -r requirements.txt
```

## 2) Настройка Telegram API и токена

1. Создай бота через [@BotFather](https://t.me/BotFather)
2. Скопируй токен
3. Получи `API_ID` и `API_HASH` на [my.telegram.org](https://my.telegram.org) (`API development tools`)
3. Создай файл `.env` на основе примера:

```bash
cp .env.example .env
```

В `.env`:

```env
BOT_TOKEN=твой_токен
API_ID=123456
API_HASH=твой_api_hash
DATABASE_URL=postgresql://user:password@localhost:5432/wav_to_mp3
MAX_INPUT_MB=50
```

## 3) Запуск

```bash
export $(grep -v '^#' .env | xargs) && python3 bot.py
```

## Использование

- Отправь боту WAV-файл **как документ**.
- Бот вернет файл `converted.mp3`.
- Лимит входного файла задается переменной `MAX_INPUT_MB` (по умолчанию 50).
- Команда `/stats` показывает:
  - сколько всего пользователей заходило,
  - сколько всего конвертаций выполнено,
  - список последних активных пользователей.

## Деплой на Railway

1. Запушь репозиторий в GitHub.
2. В Railway: `New Project` -> `Deploy from GitHub repo` -> выбери репозиторий.
3. Railway автоматически соберет `Dockerfile`.
4. В `Variables` добавь:
   - `BOT_TOKEN=твой_токен_бота`
   - `API_ID=твой_api_id`
   - `API_HASH=твой_api_hash`
   - `DATABASE_URL=${{Postgres.DATABASE_URL}}`
   - `MAX_INPUT_MB=50`
5. Нажми `Deploy`.

Как подключить Postgres в Railway:
- В проекте Railway нажми `New` -> `Database` -> `Add PostgreSQL`.
- После создания БД добавь переменную `DATABASE_URL` из секции Variables Postgres-сервиса в сервис с ботом.

Проверка:
- Открой `Deployments` и убедись, что контейнер запущен без ошибок.
- Напиши боту `/start`, затем отправь `.wav` файлом.
