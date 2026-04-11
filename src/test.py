#!/usr/bin/env python3
"""
Тестовий скрипт для перевірки функціональності парсера вакансій.
Запускається без надсилання повідомлень у Telegram та без оновлення стану.
"""

import logging
from .fetcher import fetch_job_page
from .parser import parse_jobs
from .storage import load_previous_state, find_new_jobs
from .llm import summarize_job
from .notifier import build_notification

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


def test_parser() -> None:
    """Тестує парсер: завантажує сторінку, парсить вакансії, порівнює зі станом."""
    logging.info("Тестування парсера...")
    try:
        html = fetch_job_page()
        jobs = parse_jobs(html)
        logging.info("Знайдено %d вакансій на сторінці.", len(jobs))

        for i, job in enumerate(jobs, 1):
            logging.info("%d. %s - %s", i, job['title'], job['url'])
            logging.info("   Компанія: %s | Локація: %s | Опубліковано: %s",
                        job['company'], job['location'], job['published'])

        previous_state = load_previous_state()
        new_jobs = find_new_jobs(jobs, previous_state)
        logging.info("Знайдено %d нових вакансій (порівняно з минулим станом).", len(new_jobs))

        if new_jobs:
            logging.info("Нові вакансії:")
            for job in new_jobs:
                summary = summarize_job(job)
                message = build_notification(job, summary)
                logging.info("Повідомлення:\n%s", message)

        # Показати LLM для всіх вакансій (для тестування)
        logging.info("LLM-аналіз для всіх вакансій:")
        for job in jobs:
            summary = summarize_job(job)
            logging.info("Вакансія: %s\nАналіз: %s", job['title'], summary)

        logging.info("Тест завершено успішно.")
    except Exception as error:
        logging.exception("Помилка під час тестування: %s", error)


def test_fetcher() -> None:
    """Тестує тільки завантаження сторінки."""
    logging.info("Тестування fetcher...")
    try:
        html = fetch_job_page()
        logging.info("Сторінка завантажена успішно, розмір: %d символів.", len(html))
        if "arbeidsplassen" in html.lower():
            logging.info("HTML містить очікуваний контент.")
        else:
            logging.warning("HTML не містить очікуваний контент.")
    except Exception as error:
        logging.exception("Помилка під час тестування fetcher: %s", error)


def test_storage() -> None:
    """Тестує збереження та завантаження стану."""
    logging.info("Тестування storage...")
    try:
        from storage import save_state
        html = fetch_job_page()
        jobs = parse_jobs(html)
        save_state(jobs)
        loaded = load_previous_state()
        logging.info("Збережено %d вакансій, завантажено %d.", len(jobs), len(loaded))
        if len(jobs) == len(loaded):
            logging.info("Збереження/завантаження працює коректно.")
        else:
            logging.warning("Невідповідність кількості вакансій.")
    except Exception as error:
        logging.exception("Помилка під час тестування storage: %s", error)


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        test_name = sys.argv[1]
        if test_name == "fetcher":
            test_fetcher()
        elif test_name == "storage":
            test_storage()
        elif test_name == "parser":
            test_parser()
        else:
            print("Використання: python test.py [fetcher|storage|parser]")
            print("Без аргументів - повний тест.")
            test_parser()
    else:
        test_parser()