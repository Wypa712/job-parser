# Job Parser for arbeidsplassen.nav.no

Автоматичний парсер вакансій з норвезької сайту arbeidsplassen.nav.no з Groq LLM-аналізом та сповіщеннями через Telegram.

**🚀 Статус:** **АКТИВНИЙ** - розгорнутий на GitHub Actions, працює автоматично 2 рази на день.

## ✨ Можливості

- ✅ Автоматичні перевірки вакансій 2 рази на день (6:00 та 18:00 UTC)
- 🤖 **Groq LLM-аналіз** - витягує спеціалізацію, навички, вимоги (OpenAI видалено)
- 📱 Сповіщення через Telegram з детальною інформацією
- 📝 Збереження стану в git (не дублює старі вакансії)
- 🔄 Отримання повного опису з сторінок вакансій
- 🏗️ Чиста архітектура (src/, docs/, data/)

## 🚀 Швидкий старт на GitHub Actions

### 1. Клонуй репо
```bash
git clone https://github.com/YOUR_USERNAME/job-parser.git
cd job-parser
```

### 2. Додай Secrets на GitHub

Йди в **Settings** → **Secrets and variables** → **Actions** → **New repository secret**

Додай 3 secrets:
- `GROQ_API_KEY` - від https://console.groq.com (API ключ)
- `TELEGRAM_BOT_TOKEN` - від BotFather у Telegram
- `TELEGRAM_CHAT_ID` - ID чату/каналу у Telegram

### 3. Готово! 🎉

GitHub Actions будуть автоматично запускати скрипт:
- **О 6:00 UTC** (8:00 за часовим поясом Oslo)  
- **О 18:00 UTC** (20:00 за часовим поясом Oslo)

Встав на перевірку: **Actions** → **Job Parser - Automated Checks**

## 🔧 Локальний запуск

### Встановлення залежностей
```bash
python -m venv venv
source venv/bin/activate  # або venv\Scripts\activate на Windows
pip install -r requirements.txt
```

### Налаштування `.env`
```bash
cp .env.example .env
# Заповни .env своїми ключами
```

### Запуск
```bash
python main.py test    # тестовий запуск
python main.py         # повний запуск з планувальником
```

## 📁 Структура проекту

```
demo/
├── main.py                    # Головний скрипт
├── requirements.txt           # Залежності (без OpenAI)
├── .env                       # Конфігурація (локально)
├── .env.example              # Шаблон конфігурації
├── src/                       # Python модулі
│   ├── config.py             # Конфігурація (тільки Groq)
│   ├── fetcher.py            # HTTP запити
│   ├── parser.py             # Парсинг HTML
│   ├── storage.py            # Збереження стану
│   ├── llm.py               # Groq аналіз
│   └── notifier.py          # Telegram
├── docs/                     # Документація
│   ├── README.md            # Повний опис
│   ├── READY_FOR_DEPLOYMENT.md
│   ├── DEPLOY_GITHUB_ACTIONS.md
│   └── GITHUB_ACTIONS_SETUP.md
├── data/
│   └── state.json           # Стан вакансій (в git)
├── .github/
│   └── workflows/
│       └── job-parser.yml   # GitHub Actions конфіг
└── .gitignore
```

## ⚙️ Налаштування

### Зміна розкладу
Редагуй `.github/workflows/job-parser.yml`:

```yaml
on:
  schedule:
    - cron: '0 6,18 * * *'  # 6:00 та 18:00 UTC
```

### LLM налаштування
Використовується Groq API. Налаштування в `src/llm.py`.

### Telegram налаштування
- Створи бота через @BotFather
- Отримай chat ID через @userinfobot

## 📊 Моніторинг

- **Actions вкладка** - логи всіх запусків
- **Run workflow** - ручний запуск для тестування
- **Secrets** - перевір API ключі

## 🛠️ Вирішення проблем

### Локально не працює
```bash
python -c "import sys; sys.path.insert(0, '.'); from src.config import GROQ_API_KEY; print('OK' if GROQ_API_KEY else 'No key')"
```

### На GitHub Actions помилка
- Перевір Secrets
- Перевір логи в Actions
- Перевір `.env` локально

## 📈 Статистика

- **Запуски:** 60/місяць (2/день × 30)
- **Час виконання:** ~10 секунд
- **Витрати:** 0$ (безплатно)
- **LLM:** Groq (швидкий та дешевий)

### Тестовий запуск
```bash
python main.py test
```

### Звичайний запуск
```bash
python main.py
```

## 📋 Як розпізнати чи всі налаштовано правильно

1. **GitHub Actions** - запусти вручну: **Workflow** → **Run workflow**
2. Перевір логи в **Actions** → **Job Parser - Automated Checks** → **Run details**
3. Якщо є помилки - буде яскравий ❌ в статусі

## 🐛 Розв'язання проблем

### GitHub Actions показує помилку
- Перевір, чи всі 3 Secrets додані правильно
- Переглянь логи в Actions tab для деталей помилки

### Не приходять сповіщення
- Перевір чи `TELEGRAM_BOT_TOKEN` та `TELEGRAM_CHAT_ID` правильні
- Впиши `/start` до бота перед запуском

### Залишилася питання?
Відкрий Issue на GitHub або переглянь логи у Actions

## 📊 Stack
- **Python 3.11+**
- **BeautifulSoup4** - парсинг HTML
- **Requests** - HTTP запити
- **Groq API** — LLM-аналіз (openai-сумісний інтерфейс)
- **python-telegram-bot** - сповіщення
- **APScheduler** - планування задач

## 📝 Ліцензія
MIT
