# Job Parser for arbeidsplassen.nav.no

Автоматичний парсер вакансій з норвезької сайту arbeidsplassen.nav.no з LLM-аналізом та сповіщеннями через Telegram.

## ✨ Можливості

- ✅ Автоматичні перевірки вакансій 2 рази на день
- 🤖 LLM-аналіз (Groq/OpenAI) - витягує спеціалізацію, навички, вимоги
- 📱 Сповіщення через Telegram з детальною інформацією
- 📝 Зберігання стану (не дублює старі вакансії)
- 🔄 Отримання повного опису з сторін вакансій

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
- **Groq/OpenAI** - LLM аналіз
- **python-telegram-bot** - сповіщення
- **APScheduler** - планування задач

## 📝 Ліцензія
MIT
