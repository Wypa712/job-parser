import json
import logging
from pathlib import Path
from .config import STATE_PATH

STATE_FIELDS = ("id", "title", "company", "location", "published", "summary", "url")
# Only these fields trigger a "modified" notification — volatile fields like summary are excluded
_CHANGE_DETECTION_FIELDS = ("title", "company", "location")


def _ensure_state_path():
    if not STATE_PATH.parent.exists():
        STATE_PATH.parent.mkdir(parents=True, exist_ok=True)


def _normalize_job(job: dict) -> dict:
    return {field: job.get(field, "") for field in STATE_FIELDS}


def build_state_payload(jobs: list[dict]) -> dict[str, dict]:
    return {_normalize_job(job)["id"]: _normalize_job(job) for job in jobs if job.get("id")}


def load_previous_state() -> dict:
    _ensure_state_path()
    if not STATE_PATH.exists():
        logging.info("State file not found: %s", STATE_PATH)
        return {}
    try:
        with STATE_PATH.open("r", encoding="utf-8") as handle:
            state = json.load(handle)
            logging.info("Loaded previous state with %d jobs.", len(state))
            return state
    except (json.JSONDecodeError, OSError) as error:
        logging.warning("Failed to load previous state.json: %s", error)
        return {}


def save_state(jobs: list[dict]) -> None:
    _ensure_state_path()
    payload = build_state_payload(jobs)
    temp_path = STATE_PATH.with_suffix(".tmp")
    with temp_path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2)
        handle.flush()
    import os
    os.replace(str(temp_path), str(STATE_PATH))
    logging.info("Saved state.json with %d jobs to %s", len(payload), STATE_PATH)


def find_new_jobs(current_jobs: list[dict], previous_state: dict) -> list[dict]:
    current_state = build_state_payload(current_jobs)
    previous_ids = set(previous_state.keys())
    return [current_state[job_id] for job_id in sorted(current_state.keys() - previous_ids)]


def find_changed_jobs(current_jobs: list[dict], previous_state: dict) -> dict[str, list]:
    current_state = build_state_payload(current_jobs)
    current_ids = set(current_state.keys())
    previous_ids = set(previous_state.keys())

    added = [current_state[job_id] for job_id in sorted(current_ids - previous_ids)]
    modified = [
        current_state[job_id]
        for job_id in sorted(current_ids & previous_ids)
        if any(
            current_state[job_id].get(f) != previous_state[job_id].get(f)
            for f in _CHANGE_DETECTION_FIELDS
        )
    ]
    removed = sorted(previous_ids - current_ids)

    return {
        "added": added,
        "modified": modified,
        "removed": removed,
    }
