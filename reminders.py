import logging
from datetime import date, datetime, timedelta
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup
from storage import get_all_users_plants, get_lang, get_settings
from i18n import t

logger = logging.getLogger(__name__)

async def send_hourly_reminders(bot: Bot) -> None:
    current_hour = datetime.now().hour
    all_data = get_all_users_plants()
    today = date.today()
    for user_id_str, plants in all_data.items():
        user_id = int(user_id_str)
        settings = get_settings(user_id)
        vacation_until = settings.get("vacation_until")
        if vacation_until and date.fromisoformat(vacation_until) >= today:
            continue
        if settings.get("reminder_hour", 8) != current_hour:
            continue
        due_indexed = []
        for idx, p in enumerate(plants):
            last = date.fromisoformat(p["last_watered"])
            due = last + timedelta(days=p["interval_days"])
            if due <= today:
                due_indexed.append((idx, p))
        if not due_indexed:
            continue
        lang = get_lang(user_id)
        lines = [t(lang, "reminder_header")]
        for idx, p in due_indexed:
            last = date.fromisoformat(p["last_watered"])
            due = last + timedelta(days=p["interval_days"])
            days_overdue = (today - due).days
            if days_overdue > 0:
                lines.append(t(lang, "reminder_overdue", name=p["name"], n=days_overdue))
            else:
                lines.append(t(lang, "reminder_today", name=p["name"]))
        lines.append(t(lang, "reminder_footer"))
        btn_label = t(lang, "quick_water_btn")
        buttons = [[InlineKeyboardButton(f"{btn_label} {p['name']}", callback_data=f"water:{idx}")] for idx, p in due_indexed]
        markup = InlineKeyboardMarkup(buttons)
        try:
            await bot.send_message(chat_id=user_id, text="\n".join(lines), parse_mode="Markdown", reply_markup=markup)
        except Exception as e:
            logger.warning(f"Could not send reminder to {user_id_str}: {e}")
