from datetime import date, timedelta
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from storage import (
    get_plants, add_plant, water_plant, delete_plant,
    edit_plant_interval, rename_plant, set_plant_note,
    get_lang, set_lang, get_settings, set_reminder_hour,
    set_vacation, get_streak,
)
from i18n import t, STRINGS
from plants_db import (
    search_plant, PLANT_COUNT,
    get_plants_by_category, get_plant_by_index,
    CATEGORIES_AR, CATEGORIES_EN, CATEGORY_KEYS,
)


# ── Helpers ───────────────────────────────────────────────────────────────────

def _lang(update: Update) -> str:
    return get_lang(update.effective_user.id)


def _lang_from_query(query) -> str:
    return get_lang(query.from_user.id)


def _days_until_water(plant: dict) -> int:
    last = date.fromisoformat(plant["last_watered"])
    due = last + timedelta(days=plant["interval_days"])
    return (due - date.today()).days


def _watering_freq_label(days: int, lang: str) -> str:
    if days == 1:
        return t(lang, "freq_daily")
    elif days <= 2:
        return t(lang, "freq_xday", n=days)
    elif days == 3:
        return t(lang, "freq_twice_week")
    elif days <= 6:
        return t(lang, "freq_xday", n=days)
    elif days == 7:
        return t(lang, "freq_weekly")
    elif days <= 10:
        return t(lang, "freq_xday", n=days)
    elif days == 14:
        return t(lang, "freq_twice_month")
    elif days <= 35:
        return t(lang, "freq_monthly")
    else:
        return t(lang, "freq_rare", n=days)


def _day_name(weekday: int, lang: str) -> str:
    if lang == "ar":
        return STRINGS["ar"]["days_ar"][weekday]
    return STRINGS["en"]["days_en"][weekday]


def _fmt_date(d: date, lang: str) -> str:
    return d.strftime("%d/%m/%Y")


# ── Keyboards ─────────────────────────────────────────────────────────────────

def _language_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([[
        InlineKeyboardButton("English 🇬🇧", callback_data="lang:en"),
        InlineKeyboardButton("العربية 🇸🇦", callback_data="lang:ar"),
    ]])


def _category_keyboard(lang: str) -> InlineKeyboardMarkup:
    cats = CATEGORIES_AR if lang == "ar" else CATEGORIES_EN
    keys = list(cats.keys())
    rows = []
    for i in range(0, len(keys), 2):
        row = [InlineKeyboardButton(cats[k], callback_data=f"cat:{k}") for k in keys[i:i+2]]
        rows.append(row)
    return InlineKeyboardMarkup(rows)


def _plants_keyboard(cat_key: str, lang: str) -> InlineKeyboardMarkup:
    entries = get_plants_by_category(cat_key)
    rows = []
    for i in range(0, len(entries), 2):
        row = []
        for idx, plant in entries[i:i+2]:
            label = plant["ar_name"] if lang == "ar" else plant["en_name"]
            row.append(InlineKeyboardButton(label, callback_data=f"pd:{idx}:{cat_key}"))
        rows.append(row)
    rows.append([InlineKeyboardButton(t(lang, "back_categories"), callback_data="showcat")])
    return InlineKeyboardMarkup(rows)


def _plant_detail_keyboard(cat_key: str, lang: str, plant_idx: int, already_added: bool = False) -> InlineKeyboardMarkup:
    add_label = t(lang, "added_already_btn") if already_added else t(lang, "add_from_db_btn")
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(add_label, callback_data=f"addplant:{plant_idx}")],
        [InlineKeyboardButton(t(lang, "back_to_plant_list"), callback_data=f"cat:{cat_key}")],
    ])


def _delete_confirm_keyboard(lang: str, index: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([[
        InlineKeyboardButton(t(lang, "delete_yes_btn"), callback_data=f"dodel:{index}"),
     InlineKeyboardButton(t(lang, "delete_no_btn"),  callback_data="nodol"),
    ]])


# ── /start ────────────────────────────────────────────────────────────────────

async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Choose language / اختر اللغة",
        reply_markup=_language_keyboard(),
    )


# ── Callbacks ─────────────────────────────────────────────────────────────────

async def callback_language(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    lang = query.data.split(":")[1]
    set_lang(query.from_user.id, lang)
    await query.edit_message_text(
        t(lang, "language_saved") + "\n\n" + t(lang, "welcome"),
        parse_mode="Markdown",
    )
    await query.message.reply_text(
        t(lang, "choose_category"),
        reply_markup=_category_keyboard(lang),
    )

async def callback_show_categories(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    lang = _lang_from_query(query)
    await query.edit_message_text(
        t(lang, "choose_category"),
        reply_markup=_category_keyboard(lang),
    )

async def callback_category(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    lang = _lang_from_query(query)
    cat_key = query.data.split(":")[1]
    cats = CATEGORIES_AR if lang == "ar" else CATEGORIES_EN
    cat_label = cats.get(cat_key, cat_key)
    emoji = cat_label.split()[0]
    name  = " ".join(cat_label.split()[1:])
    await query.edit_message_text(
        t(lang, "category_plants_header", emoji=emoji, name=name),
        parse_mode="Markdown",
        reply_markup=_plants_keyboard(cat_key, lang),
    )


async def callback_plant_detail(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    lang = _lang_from_query(query)
    parts = query.data.split(":")
    idx = int(parts[1])
    cat_key = parts[2] if len(parts) > 2 else "fruit"
    plant = get_plant_by_index(idx)
    if plant is None:
        await query.answer("Plant not found", show_alert=True)
        return
    category = plant["category_ar"] if lang == "ar" else plant["category_en"]
    tips     = plant["tips_ar"]     if lang == "ar" else plant["tips_en"]
    freq     = _watering_freq_label(plant["watering_days"], lang)
    await query.edit_message_text(
        t(lang, "plant_found",
          ar_name=plant["ar_name"], en_name=plant["en_name"],
          category=category, days=plant["watering_days"], freq=freq, tips=tips),
        parse_mode="Markdown",
        reply_markup=_plant_detail_keyboard(cat_key, lang, idx),
    )


async def callback_addplant(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    lang  = _lang_from_query(query)
    idx   = int(query.data.split(":")[1])
    plant = get_plant_by_index(idx)
    if plant is None:
        await query.answer("Plant not found", show_alert=True)
        return
    name  = plant["ar_name"] if lang == "ar" else plant["en_name"]
    days  = plant["watering_days"]
    freq  = _watering_freq_label(days, lang)
    next_date = _fmt_date(date.today() + timedelta(days=days), lang)
    add_plant(query.from_user.id, name, days)
    cat_ar  = plant["category_ar"]
    cat_key = next((k for k, v in CATEGORY_KEYS.items() if v == cat_ar), "fruit")
    category = plant["category_ar"] if lang == "ar" else plant["category_en"]
    tips     = plant["tips_ar"]     if lang == "ar" else plant["tips_en"]
    detail  = t(lang, "plant_found",
                ar_name=plant["ar_name"], en_name=plant["en_name"],
                category=category, days=days, freq=freq, tips=tips)
    success = t(lang, "add_from_db_success", name=name, freq=freq, days=days, date=next_date)
    await query.answer()
    await query.edit_message_text(
        detail + "\n\n─────────────\n" + success,
        parse_mode="Markdown",
        reply_markup=_plant_detail_keyboard(cat_key, lang, idx, already_added=True),
    )


async def callback_watered_quick(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    lang  = _lang_from_query(query)
    idx   = int(query.data.split(":")[1])
    plant = water_plant(query.from_user.id, idx)
    if plant is None:
        await query.answer("Plant not found", show_alert=True)
        return
    next_date = _fmt_date(date.today() + timedelta(days=plant["interval_days"]), lang)
    await query.answer(
       t(lang, "quick_water_done", name=plant["name"], date=next_date),
        show_alert=True,
    )
    old_markup = query.message.reply_markup
    if old_markup:
        new_rows = [
            row for row in old_markup.inline_keyboard
            if not any(btn.callback_data == query.data for btn in row)
        ]
        try:
            await query.edit_message_reply_markup(
                reply_markup=InlineKeyboardMarkup(new_rows) if new_rows else None
            )
        except Exception:
            pass


async def callback_confirmdelete(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    lang  = _lang_from_query(query)
    idx   = int(query.data.split(":")[1])
    removed = delete_plant(query.from_user.id, idx)
    if removed is None:
        await query.edit_message_text(t(lang, "delete_not_found", n=idx + 1))
        return
    await query.edit_message_text(
        t(lang, "delete_success", name=removed["name"]), parse_mode="Markdown"
    )


async def callback_canceldelete(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(t(_lang_from_query(query), "delete_cancelled"))


# ── Commands ──────────────────────────────────────────────────────────────────

async def cmd_plant(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    lang = _lang(update)
    if not context.args:
        await update.message.reply_text(
            t(lang, "plant_cmd_usage") + "\n\n" + t(lang, "plant_db_count", count=PLANT_COUNT),
            parse_mode="Markdown",
        )
        return
    await _do_plant_search(update, lang, " ".join(context.args))


async def cmd_search(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    lang = _lang(update)
    if not context.args:
        await update.message.reply_text(
            t(lang, "search_no_query", count=PLANT_COUNT), parse_mode="Markdown"
        )
        return
    await _do_plant_search(update, lang, " ".join(context.args))


async def _do_plant_search(update: Update, lang: str, query_str: str) -> None:
    plant = search_plant(query_str)
    if plant is None:
        await update.message.reply_text(
            t(lang, "plant_not_found", query=query_str), parse_mode="Markdown"
        )
        return
    category = plant["category_ar"] if lang == "ar" else plant["category_en"]
    tips     = plant["tips_ar"]     if lang == "ar" else plant["tips_en"]
    freq     = _watering_freq_label(plant["watering_days"], lang)
    await update.message.reply_text(
        t(lang, "plant_found",
          ar_name=plant["ar_name"], en_name=plant["en_name"],
          category=category, days=plant["watering_days"], freq=freq, tips=tips),
        parse_mode="Markdown",
    )


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Free-text handler: try searching the plant DB directly."""
    lang = _lang(update)
    text = (update.message.text or "").strip()
    if not text or len(text) < 2:
        return
    plant = search_plant(text)
    if plant:
        await _do_plant_search(update, lang, text)
    else:
        await update.message.reply_text(
            t(lang, "text_search_hint", query=text), parse_mode="Markdown"
        )


async def cmd_add(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    lang = _lang(update)
    args = context.args
    if len(args) < 2:
        await update.message.reply_text(t(lang, "add_usage"))
        return
    try:
        interval = int(args[-1])
        name = " ".join(args[:-1])
    except ValueError:
        await update.message.reply_text(t(lang, "add_days_error"))
        return
    if interval < 1:
        await update.message.reply_text(t(lang, "add_interval_error"))
        return
    plant = add_plant(update.effective_user.id, name, interval)
    freq  = _watering_freq_label(interval, lang)
    await update.message.reply_text(
        t(lang, "add_success", name=plant["name"], days=interval, freq=freq),
        parse_mode="Markdown",
    )


async def cmd_myplants(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    lang   = _lang(update)
    plants = get_plants(update.effective_user.id)
    if not plants:
        await update.message.reply_text(t(lang, "no_plants"))
        return
    lines = [t(lang, "plants_header")]
    for i, p in enumerate(plants, 1):
        days_left = _days_until_water(p)
        if days_left < 0:
            status = t(lang, "status_overdue", n=abs(days_left))
        elif days_left == 0:
            status = t(lang, "status_today")
        else:
            status = t(lang, "status_ok", n=days_left)
        freq = _watering_freq_label(p["interval_days"], lang)
        note = p.get("note", "").strip()
        if note:
            lines.append(t(lang, "plant_row_note", i=i, name=p["name"], freq=freq, status=status, note=note))
        else:
            lines.append(t(lang, "plant_row", i=i, name=p["name"], freq=freq, status=status))
    await update.message.reply_text("\n".join(lines), parse_mode="Markdown")


async def cmd_watered(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    lang = _lang(update)
    if not context.args:
        await update.message.reply_text(t(lang, "watered_usage"))
        return
    try:
        index = int(context.args[0]) - 1
    except ValueError:
        await update.message.reply_text(t(lang, "watered_number_error"))
        return
    plant = water_plant(update.effective_user.id, index)
    if plant is None:
        total = len(get_plants(update.effective_user.id))
        await update.message.reply_text(t(lang, "watered_not_found", n=index + 1, total=total))
        return
    next_due = _fmt_date(date.today() + timedelta(days=plant["interval_days"]), lang)
    await update.message.reply_text(
        t(lang, "watered_success", name=plant["name"], date=next_due),
        parse_mode="Markdown",
    )


async def cmd_delete(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    lang = _lang(update)
    if not context.args:
        await update.message.reply_text(t(lang, "delete_usage"))
        return
    try:
        index = int(context.args[0]) - 1
    except ValueError:
        await update.message.reply_text(t(lang, "delete_usage"))
        return
    plants = get_plants(update.effective_user.id)
    if index < 0 or index >= len(plants):
        await update.message.reply_text(t(lang, "delete_not_found", n=index + 1))
        return
    await update.message.reply_text(
        t(lang, "delete_confirm", name=plants[index]["name"]),
        parse_mode="Markdown",
        reply_markup=_delete_confirm_keyboard(lang, index),
    )


async def cmd_edit(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    lang = _lang(update)
    args = context.args
    if len(args) < 2:
        await update.message.reply_text(t(lang, "edit_usage"))
        return
    try:
        index    = int(args[0]) - 1
        new_days = int(args[1])
    except ValueError:
        await update.message.reply_text(t(lang, "edit_days_error"))
        return
    plant = edit_plant_interval(update.effective_user.id, index, new_days)
    if plant is None:
        total = len(get_plants(update.effective_user.id))
        await update.message.reply_text(t(lang, "edit_not_found", n=index + 1, total=total))
        return
    freq = _watering_freq_label(new_days, lang)
    await update.message.reply_text(
        t(lang, "edit_success", name=plant["name"], freq=freq, days=new_days),
        parse_mode="Markdown",
    )


async def cmd_rename(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    lang = _lang(update)
    args = context.args
    if len(args) < 2:
        await update.message.reply_text(t(lang, "rename_usage"))
        return
    try:
        index = int(args[0]) - 1
        new_name = " ".join(args[1:])
    except ValueError:
        await update.message.reply_text(t(lang, "rename_usage"))
        return
    plant = rename_plant(update.effective_user.id, index, new_name)
    if plant is None:
        await update.message.reply_text(t(lang, "rename_not_found", n=index + 1))
        return
    await update.message.reply_text(
        t(lang, "rename_success", name=plant["name"]), parse_mode="Markdown"
    )


async def cmd_note(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    lang = _lang(update)
    args = context.args
    if len(args) < 1:
        await update.message.reply_text(t(lang, "note_usage"))
        return
    try:
        index = int(args[0]) - 1
    except ValueError:
        await update.message.reply_text(t(lang, "note_usage"))
        return
    note_text = " ".join(args[1:]).strip()
    plant = set_plant_note(update.effective_user.id, index, note_text)
    if plant is None:
        await update.message.reply_text(t(lang, "note_not_found", n=index + 1))
        return
    if note_text:
        await update.message.reply_text(
            t(lang, "note_success", name=plant["name"], note=note_text),
            parse_mode="Markdown",
        )
    else:
        await update.message.reply_text(
            t(lang, "note_cleared", name=plant["name"]), parse_mode="Markdown"
        )


async def cmd_vacation(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    lang = _lang(update)
    settings = get_settings(update.effective_user.id)

    # No args → show current status
    if not context.args:
        vacation_until = settings.get("vacation_until")
        if vacation_until and date.fromisoformat(vacation_until) >= date.today():
            await update.message.reply_text(
                t(lang, "vacation_active", until=vacation_until), parse_mode="Markdown"
            )
        else:
            await update.message.reply_text(t(lang, "vacation_usage"))
        return

    try:
        days = int(context.args[0])
    except ValueError:
        await update.message.reply_text(t(lang, "vacation_days_error"))
        return

    if days <= 0:
        set_vacation(update.effective_user.id, 0)
        await update.message.reply_text(t(lang, "vacation_cancelled"))
    else:
        set_vacation(update.effective_user.id, days)
        until = (date.today() + timedelta(days=days)).strftime("%d/%m/%Y")
        await update.message.reply_text(
            t(lang, "vacation_set", days=days, until=until), parse_mode="Markdown"
        )


async def cmd_schedule(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    lang   = _lang(update)
    plants = get_plants(update.effective_user.id)
    if not plants:
        await update.message.reply_text(t(lang, "schedule_no_plants"))
        return

    today = date.today()
    lines = [t(lang, "schedule_header")]

    for offset in range(7):
        target = today + timedelta(days=offset)
        day_name = _day_name(target.weekday(), lang)

        if offset == 0:
            header = t(lang, "schedule_today", day=day_name)
            # Today = overdue + due today
            due = [p["name"] for p in plants if _days_until_water(p) <= 0]
        else:
            header = t(lang, "schedule_day", day=day_name)
            due = [p["name"] for p in plants if _days_until_water(p) == offset]

        if due:
            lines.append(f"\n{header}")
            for name in due:
                lines.append(f"  💧 {name}")
        else:
            lines.append(f"\n{header}")
            lines.append(f"  {t(lang, 'schedule_empty_day')}")

    await update.message.reply_text("\n".join(lines), parse_mode="Markdown")


async def cmd_next(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    lang   = _lang(update)
    plants = get_plants(update.effective_user.id)
    if not plants:
        await update.message.reply_text(t(lang, "no_plants"))
        return

    today = date.today()
    overdue, due_today, upcoming = [], [], {}

    for p in plants:
        days_left = _days_until_water(p)
        if days_left < 0:
            overdue.append(p["name"])
        elif days_left == 0:
            due_today.append(p["name"])
        elif days_left <= 7:
            upcoming.setdefault(days_left, []).append(p["name"])

    lines = [t(lang, "next_header")]
    if overdue:
        lines.append(t(lang, "next_overdue", names=", ".join(overdue)))
    if due_today:
        lines.append(t(lang, "next_today", names=", ".join(due_today)))
    for n in sorted(upcoming):
        day_name = _day_name((today + timedelta(days=n)).weekday(), lang)
        if n == 1:
            lines.append(t(lang, "next_tomorrow", names=", ".join(upcoming[n])))
        else:
            lines.append(t(lang, "next_day", n=n, day=day_name, names=", ".join(upcoming[n])))

    if not overdue and not due_today and not upcoming:
        lines.append(t(lang, "next_all_ok"))

    await update.message.reply_text("\n".join(lines), parse_mode="Markdown")


async def cmd_stats(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    lang   = _lang(update)
    plants = get_plants(update.effective_user.id)
    if not plants:
        await update.message.reply_text(t(lang, "stats_empty"))
        return

    overdue_count = today_count = ok_count = 0
    total_waterings = 0
    next_name = ""
    next_days_left = 9999

    for p in plants:
        days_left = _days_until_water(p)
        total_waterings += p.get("total_waterings", 0)
        if days_left < 0:
            overdue_count += 1
        elif days_left == 0:
            today_count += 1
        else:
            ok_count += 1
            if days_left < next_days_left:
                next_days_left = days_left
                next_name = p["name"]

    streak = get_streak(update.effective_user.id)
    next_info = (
        t(lang, "stats_no_next") if not next_name
        else (f"{next_days_left}d" if lang == "en" else f"{next_days_left} يوم")
    )

    await update.message.reply_text(
        t(lang, "stats_header") + t(
            lang, "stats_body",
            total=len(plants), ok=ok_count, today=today_count, overdue=overdue_count,
            waterings=total_waterings, streak=streak,
            next_name=next_name or "—", next_days=next_info,
        ),
        parse_mode="Markdown",
    )


async def cmd_export(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    lang   = _lang(update)
    plants = get_plants(update.effective_user.id)
    if not plants:
        await update.message.reply_text(t(lang, "export_empty"))
        return

    today_str = date.today().strftime("%d/%m/%Y")
    lines = [t(lang, "export_header", date=today_str)]

    for i, p in enumerate(plants, 1):
        freq = _watering_freq_label(p["interval_days"], lang)
        last = date.fromisoformat(p["last_watered"])
        next_d = last + timedelta(days=p["interval_days"])
        note = p.get("note", "").strip()
        row_key = "export_row_note" if note else "export_row"
        kwargs = dict(
            i=i, name=p["name"], freq=freq, days=p["interval_days"],
            last=_fmt_date(last, lang), next=_fmt_date(next_d, lang),
        )
        if note:
            kwargs["note"] = note
        lines.append(t(lang, row_key, **kwargs))

    from plants_db import PLANT_COUNT
    lines.append(t(lang, "export_footer", count=PLANT_COUNT))
    await update.message.reply_text("\n\n".join(lines), parse_mode="Markdown")


async def cmd_reminder(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    lang = _lang(update)
    if not context.args:
        current = get_settings(update.effective_user.id).get("reminder_hour", 8)
        await update.message.reply_text(
            t(lang, "reminder_usage") + f"\n\n⏰ Current: *{current:02d}:00*",
            parse_mode="Markdown",
        )
        return
    try:
        hour = int(context.args[0])
        if not 0 <= hour <= 23:
            raise ValueError
    except ValueError:
        await update.message.reply_text(t(lang, "reminder_invalid"))
        return
    set_reminder_hour(update.effective_user.id, hour)
    await update.message.reply_text(
        t(lang, "reminder_set", hour=f"{hour:02d}"), parse_mode="Markdown"
    )
