import json
import os
from datetime import date, timedelta

DATA_FILE     = os.path.join(os.path.dirname(__file__), "plants.json")
LANG_FILE     = os.path.join(os.path.dirname(__file__), "languages.json")
SETTINGS_FILE = os.path.join(os.path.dirname(__file__), "settings.json")


# ── Internal helpers ──────────────────────────────────────────────────────────

def _load() -> dict:
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r") as f:
        return json.load(f)


def _save(data: dict) -> None:
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def _load_langs() -> dict:
    if not os.path.exists(LANG_FILE):
        return {}
    with open(LANG_FILE, "r") as f:
        return json.load(f)


def _save_langs(data: dict) -> None:
    with open(LANG_FILE, "w") as f:
        json.dump(data, f, indent=2)


def _load_settings() -> dict:
    if not os.path.exists(SETTINGS_FILE):
        return {}
    with open(SETTINGS_FILE, "r") as f:
        return json.load(f)


def _save_settings(data: dict) -> None:
    with open(SETTINGS_FILE, "w") as f:
        json.dump(data, f, indent=2)


# ── Language ──────────────────────────────────────────────────────────────────

def get_lang(user_id: int) -> str:
    return _load_langs().get(str(user_id), "en")


def set_lang(user_id: int, lang: str) -> None:
    langs = _load_langs()
    langs[str(user_id)] = lang
    _save_langs(langs)


# ── Settings ──────────────────────────────────────────────────────────────────

def get_settings(user_id: int) -> dict:
    return _load_settings().get(str(user_id), {"reminder_hour": 8})


def _update_settings(user_id: int, updates: dict) -> None:
    settings = _load_settings()
    key = str(user_id)
    if key not in settings:
        settings[key] = {}
    settings[key].update(updates)
    _save_settings(settings)


def set_reminder_hour(user_id: int, hour: int) -> None:
    _update_settings(user_id, {"reminder_hour": hour})


def set_vacation(user_id: int, days: int) -> None:
    if days <= 0:
        _update_settings(user_id, {"vacation_until": None})
    else:
        until = (date.today() + timedelta(days=days)).isoformat()
        _update_settings(user_id, {"vacation_until": until})


def get_all_settings() -> dict:
    return _load_settings()


# ── Streak helpers (called inside water_plant) ────────────────────────────────

def _update_streak(user_id: int) -> int:
    settings = _load_settings()
    key = str(user_id)
    user_s = settings.get(key, {})
    today_str = date.today().isoformat()
    yesterday_str = (date.today() - timedelta(days=1)).isoformat()

    last_action = user_s.get("last_watered_date")
    streak = user_s.get("streak", 0)

    if last_action == today_str:
        pass  # already counted today
    elif last_action == yesterday_str:
        streak += 1
    else:
        streak = 1

    user_s["last_watered_date"] = today_str
    user_s["streak"] = streak
    settings[key] = user_s
    _save_settings(settings)
    return streak


def get_streak(user_id: int) -> int:
    return get_settings(user_id).get("streak", 0)


# ── Plants ────────────────────────────────────────────────────────────────────

def get_plants(user_id: int) -> list[dict]:
    return _load().get(str(user_id), [])


def add_plant(user_id: int, name: str, interval_days: int) -> dict:
    data = _load()
    key = str(user_id)
    if key not in data:
        data[key] = []
    plant = {
        "name": name,
        "interval_days": interval_days,
        "last_watered": date.today().isoformat(),
        "total_waterings": 0,
        "added_on": date.today().isoformat(),
        "note": "",
    }
    data[key].append(plant)
    _save(data)
    return plant


def water_plant(user_id: int, index: int) -> dict | None:
    data = _load()
    key = str(user_id)
    plants = data.get(key, [])
    if index < 0 or index >= len(plants):
        return None
    plants[index]["last_watered"] = date.today().isoformat()
    plants[index]["total_waterings"] = plants[index].get("total_waterings", 0) + 1
    data[key] = plants
    _save(data)
    _update_streak(user_id)
    return plants[index]


def delete_plant(user_id: int, index: int) -> dict | None:
    data = _load()
    key = str(user_id)
    plants = data.get(key, [])
    if index < 0 or index >= len(plants):
        return None
    removed = plants.pop(index)
    data[key] = plants
    _save(data)
    return removed


def edit_plant_interval(user_id: int, index: int, new_days: int) -> dict | None:
    data = _load()
    key = str(user_id)
    plants = data.get(key, [])
    if index < 0 or index >= len(plants):
        return None
    plants[index]["interval_days"] = new_days
    data[key] = plants
    _save(data)
    return plants[index]


def rename_plant(user_id: int, index: int, new_name: str) -> dict | None:
    data = _load()
    key = str(user_id)
    plants = data.get(key, [])
    if index < 0 or index >= len(plants):
        return None
    plants[index]["name"] = new_name
    data[key] = plants
    _save(data)
    return plants[index]


def set_plant_note(user_id: int, index: int, note: str) -> dict | None:
    data = _load()
    key = str(user_id)
    plants = data.get(key, [])
    if index < 0 or index >= len(plants):
        return None
    plants[index]["note"] = note
    data[key] = plants
    _save(data)
    return plants[index]


def get_all_users_plants() -> dict:
    return _load()
