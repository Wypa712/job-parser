import asyncio
import logging
from telegram import Bot
from telegram.error import TelegramError
from .config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID


def send_telegram_message(text: str) -> None:
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        logging.warning("Telegram bot token or chat ID is not configured. Skipping notification.")
        return

    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    try:
        asyncio.run(
            bot.send_message(
                chat_id=TELEGRAM_CHAT_ID,
                text=text,
                parse_mode="HTML",
                disable_web_page_preview=True,
            )
        )
        logging.info("Telegram notification sent.")
    except TelegramError as error:
        logging.exception("Failed to send Telegram message: %s", error)


def build_notification(job: dict, summary: str = None) -> str:
    lines = [f"<b>{job.get('title')}</b>"]
    if job.get("company"):
        lines.append(f"<i>{job.get('company')}</i>")
    if job.get("location"):
        lines.append(f"<b>Локація:</b> {job.get('location')}")
    if job.get("published"):
        lines.append(f"<b>Опубліковано:</b> {job.get('published')}")
    if summary:
        lines.append(f"<b>LLM-аналітика:</b>\n{summary}")
    lines.append(f"<b>Посилання:</b> {job.get('url')}")
    return "\n".join(lines)
