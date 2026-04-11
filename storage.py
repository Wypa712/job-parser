import json
from pathlib import Path
from config import STATE_PATH


def _ensure_state_path():
    if not STATE_PATH.parent.exists():
        STATE_PATH.parent.mkdir(parents=True, exist_ok=True)


def load_previous_state() -> dict:
    _ensure_state_path()
    if not STATE_PATH.exists():
        return {}
    try:
        with STATE_PATH.open("r", encoding="utf-8") as handle:
            return json.load(handle)
    except (json.JSONDecodeError, OSError):
        return {}


def save_state(jobs: list[dict]) -> None:
    _ensure_state_path()
    payload = {job["id"]: job for job in jobs}
    with STATE_PATH.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2)


def find_new_jobs(current_jobs: list[dict], previous_state: dict) -> list[dict]:
    previous_ids = set(previous_state.keys())
    return [job for job in current_jobs if job["id"] not in previous_ids]
