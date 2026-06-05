import logging
import traceback
import os
from telegram import BotCommand, Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, CallbackQueryHandler,
    MessageHandler, filters, Application, ContextTypes,
)
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from commands import (
    cmd_start, cmd_add, cmd_myplants, cmd_watered, cmd_plant, cmd_search,
    cmd_delete, cmd_edit, cmd_stats, cmd_reminder,
    cmd_rename, cmd_note, cmd_vacation, cmd_schedule, cmd_next, cmd_export,
    callback_language, callback_show_categories,
    callback_category, callback_plant_detail,
    callback_addplant, callback_watered_quick,
    callback_confirmdelete, callback_canceldelete,
    handle_text,
)
from reminders import send_hourly_reminders
from storage import get_lang

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

BOT_COMMANDS_EN = [
    BotCommand("start",    "Choose language & browse plant categories"),
    BotCommand("search",   "Search any plant — see watering schedule"),
    BotCommand("myplants", "Your plants with watering schedule"),
    BotCommand("schedule", "Weekly watering calendar"),
    BotCommand("next",     "What needs watering soon"),
    BotCommand("watered",  "Mark a plant as watered today"),
    BotCommand("stats",    "Your plant care statistics"),
    BotCommand("add",      "Add a plant manually"),
    BotCommand("delete",   "Remove a plant from your list"),
    BotCommand("edit",     "Change a plant's watering interval"),
    BotCommand("rename",   "Rename a plant"),
    BotCommand("note",     "Add a note to a plant"),
    BotCommand("vacation", "Pause reminders while away"),
    BotCommand("export",   "Export your plant list"),
    BotCommand("reminder", "Set your daily reminder time"),
]

BOT_COMMANDS_AR = [
    BotCommand("start",    "اختر اللغة وتصفح فئات النباتات"),
    BotCommand("search",   "ابحث عن أي نبات وشوف جدول سقيه"),
    BotCommand("myplants", "نباتاتك مع جدول السقي الكامل"),
    BotCommand("schedule", "جدول السقي الأسبوعي"),
    BotCommand("next",     "أقرب مواعيد السقي"),
    BotCommand("watered",  "أشّر على نبات تم سقيه اليوم"),
    BotCommand("stats",    "إحصائيات عنايتك بالنباتات"),
    BotCommand("add",      "أضف نباتاً يدوياً"),
    BotCommand("delete",   "احذف نباتاً من قائمتك"),
    BotCommand("edit",     "غيّر جدول سقي نبات"),
    BotCommand("rename",   "غيّر اسم نبات"),
    BotCommand("note",     "أضف ملاحظة لنبات"),
    BotCommand("vacation", "وقّف التذكيرات أثناء السفر"),
    BotCommand("export",   "تصدير قائمة نباتاتك"),
    BotCommand("reminder", "خصص وقت التذكير اليومي"),
]


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.error("Exception while handling update:", exc_info=context.error)
    logger.error("".join(traceback.format_exception(
        type(context.error), context.error, context.error.__traceback__
    )))
    try:
        if isinstance(update, Update):
            user_id = update.effective_user.id if update.effective_user else None
            lang = get_lang(user_id) if user_id else "en"
            msg = (
                "⚠️ حدث خطأ، يرجى المحاولة مجدداً.\nإذا تكرر استخدم /start"
                if lang == "ar" else
                "⚠️ Something went wrong. Please try again.\nIf this keeps happening, use /start"
            )
            if update.message:
                await update.message.reply_text(msg)
            elif update.callback_query:
                await update.callback_query.answer(msg, show_alert=True)
    except Exception:
        pass


async def post_init(app: Application) -> None:
    await app.bot.set_my_commands(BOT_COMMANDS_EN)
    await app.bot.set_my_commands(BOT_COMMANDS_AR, language_code="ar")
    logger.info("Bot commands registered with Telegram.")

    scheduler = AsyncIOScheduler()
    scheduler.add_job(
        send_hourly_reminders,
        trigger="cron",
        hour="*",
        minute=0,
        args=[app.bot],
    )
    scheduler.start()
    logger.info("Hourly reminder scheduler started.")


def main() -> None:
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    if not token:
        raise RuntimeError("TELEGRAM_BOT_TOKEN environment variable is not set")

    app = ApplicationBuilder().token(token).post_init(post_init).build()

    # ── Commands ──────────────────────────────────────────────────────────────
    app.add_handler(CommandHandler("start",    cmd_start))
    app.add_handler(CommandHandler("plant",    cmd_plant))
    app.add_handler(CommandHandler("search",   cmd_search))
    app.add_handler(CommandHandler("add",      cmd_add))
    app.add_handler(CommandHandler("myplants", cmd_myplants))
    app.add_handler(CommandHandler("watered",  cmd_watered))
    app.add_handler(CommandHandler("delete",   cmd_delete))
    app.add_handler(CommandHandler("edit",     cmd_edit))
    app.add_handler(CommandHandler("rename",   cmd_rename))
    app.add_handler(CommandHandler("note",     cmd_note))
    app.add_handler(CommandHandler("vacation", cmd_vacation))
    app.add_handler(CommandHandler("schedule", cmd_schedule))
    app.add_handler(CommandHandler("next",     cmd_next))
    app.add_handler(CommandHandler("stats",    cmd_stats))
    app.add_handler(CommandHandler("export",   cmd_export))
    app.add_handler(CommandHandler("reminder", cmd_reminder))

    # ── Inline callbacks ──────────────────────────────────────────────────────
    app.add_handler(CallbackQueryHandler(callback_language,        pattern=r"^lang:"))
    app.add_handler(CallbackQueryHandler(callback_show_categories, pattern=r"^showcat$"))
    app.add_handler(CallbackQueryHandler(callback_category,        pattern=r"^cat:"))
    app.add_handler(CallbackQueryHandler(callback_plant_detail,    pattern=r"^pd:"))
    app.add_handler(CallbackQueryHandler(callback_addplant,        pattern=r"^addplant:"))
    app.add_handler(CallbackQueryHandler(callback_watered_quick,   pattern=r"^water:"))
    app.add_handler(CallbackQueryHandler(callback_confirmdelete,   pattern=r"^dodel:"))
    app.add_handler(CallbackQueryHandler(callback_canceldelete,    pattern=r"^nodol$"))

    # ── Free-text search (must be last) ───────────────────────────────────────
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    # ── Global error handler ──────────────────────────────────────────────────
    app.add_error_handler(error_handler)

    logger.info("Plant Care Bot is running...")
    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
