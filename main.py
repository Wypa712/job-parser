import logging
from datetime import datetime
from zoneinfo import ZoneInfo

from apscheduler.schedulers.blocking import BlockingScheduler

from src.fetcher import fetch_job_page
from src.parser import parse_jobs, get_full_job_description
from src.storage import find_changed_jobs, load_previous_state, save_state
from src.llm import summarize_job
from src.notifier import build_notification, send_telegram_message
from src.config import SCHEDULE_TIMES

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

JOB_TIMEZONE = ZoneInfo("Europe/Oslo")


def check_jobs(test_mode=False) -> None:
    logging.info("Починаю перевірку вакансій...")
    jobs = None
    try:
        html = fetch_job_page()
        jobs = parse_jobs(html)
        previous_state = load_previous_state()
        job_changes = find_changed_jobs(jobs, previous_state)

        if test_mode:
            logging.info("Тестовий режим: знайдено %d вакансій на сторінці.", len(jobs))
            for job in jobs:
                logging.info("Вакансія: %s - %s", job['title'], job['url'])
            return

        added_jobs = job_changes["added"]
        modified_jobs = job_changes["modified"]
        removed_jobs = job_changes["removed"]

        if not (added_jobs or modified_jobs or removed_jobs):
            logging.info("Змін у списку вакансій не виявлено.")
            return

        if added_jobs:
            logging.info("Знайдено %d нових вакансій.", len(added_jobs))
        if modified_jobs:
            logging.info("Знайдено %d оновлених вакансій.", len(modified_jobs))
        if removed_jobs:
            logging.info("Вилучено %d вакансій зі списку.", len(removed_jobs))

        for job in added_jobs + modified_jobs:
            logging.info("Отримуємо повний опис для вакансії: %s", job['title'])
            full_description = get_full_job_description(job['url'])
            job['full_description'] = full_description
            summary = summarize_job(job)
            message = build_notification(job, summary)
            send_telegram_message(message)
    except Exception as error:
        logging.exception("Помилка під час перевірки вакансій: %s", error)
    finally:
        if jobs is not None and not test_mode:
            try:
                save_state(jobs)
            except Exception as error:
                logging.exception("Не вдалося зберегти стан вакансій: %s", error)


def schedule_jobs() -> None:
    scheduler = BlockingScheduler(timezone=JOB_TIMEZONE)
    for time_value in SCHEDULE_TIMES:
        hour, minute = map(int, time_value.split(":"))
        scheduler.add_job(
            check_jobs,
            trigger="cron",
            hour=hour,
            minute=minute,
            id=f"job-check-{hour:02d}-{minute:02d}",
        )
        logging.info("Заплановано перевірку на %s.", time_value)

    logging.info("Запуск планувальника...")
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        logging.info("Планувальник зупинено.")


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        check_jobs(test_mode=True)
    else:
        check_jobs()
        schedule_jobs()
