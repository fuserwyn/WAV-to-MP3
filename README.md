# WAV to MP3 Telegram Bot

Телеграм-бот, который принимает `.wav` файл и отправляет обратно `.mp3`.

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

## 2) Настройка токена

1. Создай бота через [@BotFather](https://t.me/BotFather)
2. Скопируй токен
3. Создай файл `.env` на основе примера:

```bash
cp .env.example .env
```

В `.env`:

```env
BOT_TOKEN=твой_токен
```

## 3) Запуск

```bash
export $(grep -v '^#' .env | xargs) && python3 bot.py
```

## Использование

- Отправь боту WAV-файл **как документ**.
- Бот вернет файл `converted.mp3`.

## Деплой на Railway

1. Запушь репозиторий в GitHub.
2. В Railway: `New Project` -> `Deploy from GitHub repo` -> выбери репозиторий.
3. Railway автоматически соберет `Dockerfile`.
4. В `Variables` добавь:
   - `BOT_TOKEN=твой_токен_бота`
5. Нажми `Deploy`.

Проверка:
- Открой `Deployments` и убедись, что контейнер запущен без ошибок.
- Напиши боту `/start`, затем отправь `.wav` файлом.
