# 📝 Job Parser for arbeidsplassen.nav.no

[![GitHub Actions Status](https://github.com/Wypa712/job-parser/actions/workflows/job-parser.yml/badge.svg)](https://github.com/Wypa712/job-parser/actions)

Цей проєкт — автоматизований парсер вакансій з норвезького сайту [arbeidsplassen.nav.no](https://arbeidsplassen.nav.no). Він знаходить нові та оновлені оголошення, аналізує їх за допомогою **Groq LLM** і миттєво інформує вас через **Telegram**. 

Проєкт розроблено так, щоб повністю безкоштовно та автоматично працювати на платформі **GitHub Actions**.

---

## 🌟 Можливості

- 🔍 **Автоматичний моніторинг**: Регулярний пошук вакансій за розкладом.
- 🧠 **Smart-аналіз (Groq LLM)**: Автоматичне отримання спеціалізації, обов'язків, навичок та вимог прямо у вашому Telegram без зайвої води.
- 📱 **Telegram-сповіщення**: Акуратні повідомлення з найважливішим (Компанія, локація, деталі + посилання).
- 💾 **Пам'ять про попередні запуски**: Бот зберігає стан (state.json), щоб не надсилати одні й ті самі вакансії повторно.
- ☁️ **Full Serverless**: Все безкоштовно крутиться в GitHub Actions. Не треба орендувати власні сервери!

---

## 🏗 Архітектура проєкту

```text
job-parser/
├── main.py                     # 🚀 Головний скрипт з логікою
├── requirements.txt            # 📦 Залежності
├── .env.example                # 🔑 Шаблон для створення ключів API
├── data/
│   └── state.json              # 🗂 База (збереження стану вакансій)
├── docs/                       
│   └── GITHUB_ACTIONS.md       # 📖 Інструкції по налаштуванню GitHub Actions
├── src/                        # 🧩 Модулі
│   ├── config.py               # Конфіги, змінні оточення
│   ├── fetcher.py              # Завантаження HTML
│   ├── parser.py               # Витягування даних
│   ├── llm.py                  # Аналіз тексту через Groq API
│   ├── notifier.py             # Відправка повідомлень Telegram
│   └── test.py                 # Скрипт для тестування парсера
└── .github/workflows/          
    └── job-parser.yml          # ⚙️ Конфігурація CI/CD (GitHub Actions)
```

---

## 💻 Локальний запуск (Без GitHub Actions)

Якщо ви хочете запустити проєкт локально на своєму ПК чи сервері, використовуйте цю інструкцію. Якщо вам потрібен безкоштовний деплой — перейдіть до [**нашого гайду по деплою в GitHub Actions**](docs/GITHUB_ACTIONS.md).

### 1. Налаштування середовища і ключів

Відкрийте термінал і схиліть репозиторій. Потім:

```bash
# Скопіюйте приклад та заповніть API ключі (отримайте ключі для Groq та Telegram-бота)
cp .env.example .env

# Встановіть залежності
pip install -r requirements.txt
```

Відкрийте файл `.env` і додайте туди свої ключі:
- `GROQ_API_KEY`: Ключ від [Groq Console](https://console.groq.com)
- `TELEGRAM_BOT_TOKEN`: Від бота [@BotFather](https://t.me/BotFather)
- `TELEGRAM_CHAT_ID`: Ваш особистий ID від [@userinfobot](https://t.me/userinfobot)

### 2. Режими роботи

У вас є 3 варіанти запуску програми `main.py`:

```bash
# 1. ТЕСТОВИЙ РЕЖИМ
# Найкращий для перевірки. Виводить вакансії в консоль, нічого НЕ ЗБЕРІГАЄ.
python main.py test

# 2. ОДНА ПЕРЕВІРКА І ВИХІД
# Завантажує вакансії, зберігає в state.json і завершує роботу.
# Саме він використовується в GitHub Actions.
python main.py

# 3. БЕЗПЕРЕРВНИЙ РОЗКЛАД (APScheduler)
# Локальний планувальник крутиться вічно та перевіряє вакансії о 10:00 та 16:00
python main.py schedule
```

---

## 🧪 Запуск тестів 

Ви можете перевіряти окремі модулі проєкту, використовуючи файл `src/test.py`:

```bash
# Повний тест
python -m src.test

# Тест лише завантаження HTML:
python -m src.test fetcher

# Тест парсингу:
python -m src.test parser

# Тест збереження даних:
python -m src.test storage
```
