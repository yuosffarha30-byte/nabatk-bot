STRINGS = {
    "en": {
        "welcome": (
            "🌱 *Plant Care Bot*\n\n"
            "I'll help you remember to water your plants!\n\n"
            "*Commands:*\n"
            "/search `<name>` — Search 358+ plants\n"
            "/myplants — Your plants with watering schedule\n"
            "/schedule — Weekly watering calendar\n"
            "/next — What needs watering soon\STRINGS        "/add `<name> <days>` — Add a plant manually\n"
            "/watered `<number>` — Mark plant as watered\n"
            "/delete `<number>` — Remove a plant\n"
            "/edit `<number> <days>` — Change watering interval\n"
            "/rename `<number> <new name>` — Rename a plant\n"
            "/note `<number> <text>` — Add a note to a plant\n"
            "/vacation `<days>` — Pause reminders\n"
            "/stats — Your plant care statistics\n"
            "/export — Export your plant list\n"
            "/reminder `<hour>` — Set daily reminder time\n\n"
            "_Or just type a plant name to look it up!_"
        ),
        "language_saved": "✅ Language set to English.",
        "choose_category": "🌿 Choose a plant category to browse:",
        "category_plants_header": "{emoji} *{name}*\n\nChoose a plant to see care details:",
        "back_categories": "⬅️ Back to categories",
        "back_to_plant_list": "⬅️ Back to list",

        # Add plant
        "add_usage": "Usage: /add <plant name> <days>\nExample: /add Monstera 7",
        "add_days_error": "Last argument must be number of days.\nExample: /add Monstera 7",
        "add_interval_error": "Watering interval must be at least 1 day.",
        "add_success": "✅ Added *{name}*\n💧 {freq} (every {days} days)",

        # My plants
        "no_plants": (
            "🌵 You have no plants yet.\n\n"
            "Browse categories above, or:\n"
            "/add <name> <days>"
        ),
        "plants_header": "🪴 *Your Plants:*\n",
        "plant_row": "{i}. *{name}*\n   💧 {freq}  |  {status}",
        "plant_row_note": "{i}. *{name}*\n   💧 {freq}  |  {status}\n   📝 {note}",
        "status_overdue": "⚠️ overdue {n}d!",
        "status_today": "💧 water TODAY!",
        "status_ok": "✅ in {n} day(s)",

        # Watered
        "watered_usage": "Usage: /watered <plant number>\nSee numbers with /myplants",
        "watered_number_error": "Provide a plant number, e.g. /watered 1",
        "watered_not_found": "Plant #{n} not found. You have {total} plant(s).",
        "watered_success": "💧 *{name}* watered! ✅\nNext watering: *{date}*",

        # Delete
        "delete_usage": "Usage: /delete <plant number>\nExample: /delete 2",
        "delete_confirm": "⚠️ Delete *{name}*?\nThis cannot be undone.",
        "delete_yes_btn": "🗑️ Yes, delete",
        "delete_no_btn": "❌ Cancel",
        "delete_success": "🗑️ *{name}* removed.",
        "delete_not_found": "Plant #{n} not found.",
        "delete_cancelled": "✅ Cancelled — plant kept.",

        # Edit
        "edit_usage": "Usage: /edit <number> <days>\nExample: /edit 1 5",
        "edit_days_error": "Provide: /edit <number> <days>\nExample: /edit 1 10",
        "edit_not_found": "Plant #{n} not found. You have {total} plant(s).",
        "edit_success": "✅ *{name}* updated!\n💧 Now: {freq} (every {days} days)",

        # Rename
        "rename_usage": "Usage: /rename <number> <new name>\nExample: /rename 1 My Cactus",
        "rename_not_found": "Plant #{n} not found.",
        "rename_success": "✅ Renamed to *{name}*!",

        # Note
        "note_usage": "Usage: /note <number> <text>\nExample: /note 1 Near the window",
        "note_not_found": "Plant #{n} not found.",
        "note_success": "📝 Note added to *{name}*:\n_{note}_",
        "note_cleared": "📝 Note cleared for *{name}*.",

        # Vacation
        "vacation_usage": "Usage: /vacation <days>\nExample: /vacation 7\nUse /vacation 0 to cancel.",
        "vacation_set": "🏖️ Vacation mode on for *{days}* days.\nReminders paused until *{until}*.",
        "vacation_cancelled": "✅ Vacation mode off — reminders resumed!",
        "vacation_active": "🏖️ Vacation mode active until *{until}*.\nUse /vacation 0 to cancel.",
        "vacation_days_error": "Please provide number of days, e.g. /vacation 7",

        # Schedule
        "schedule_header": "📅 *Weekly Watering Schedule:*\n",
        "schedule_today": "📍 Today ({day}):",
        "schedule_day": "📅 {day}:",
        "schedule_empty_day": "✅ No watering",
        "schedule_no_plants": "No plants yet! Add some with /add or browse categories.",
        "days_en": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],

        # Next
        "next_header": "📅 *Upcoming Waterings:*\n",
        "next_today": "💧 Today: {names}",
        "next_tomorrow": "📅 Tomorrow: {names}",
        "next_day": "📅 In {n} days ({day}): {names}",
        "next_all_ok": "✅ All plants are on schedule!\nEverything watered recently.",
        "next_overdue": "⚠️ Overdue: {names}",

        # Stats
        "stats_header": "📊 *Your Plant Stats:*\n",
        "stats_body": (
            "🌱 Total plants: *{total}*\n"
            "✅ On schedule: *{ok}*\n"
            "💧 Due today: *{today}*\n"
            "⚠️ Overdue: *{overdue}*\n\n"
            "💦 Total waterings logged: *{waterings}*\n"
            "🔥 Watering streak: *{streak} day(s)*\n"
            "📅 Next due: *{next_name}* ({next_days})"
        ),
        "stats_no_next": "all on schedule!",
        "stats_empty": "No plants yet. Add some with /add or browse categories!",

        # Reminder
        "reminder_usage": "Usage: /reminder <hour (0–23)>\nExample: /reminder 9",
        "reminder_invalid": "Please provide a valid hour between 0 and 23.",
        "reminder_set": "⏰ Reminder set for *{hour}:00* every day.",

        # Reminder message
        "reminder_header": "💧 *Time to water your plants!*\n",
        "reminder_overdue": "⚠️ *{name}* — {n} day(s) overdue!",
        "reminder_today": "🌱 *{name}* — water today",
        "reminder_footer": "\nTap a button or use /watered <number>.",
        "quick_water_btn": "💧 Watered",
        "quick_water_done": "✅ {name} watered!\nNext: {date}",

        # Export
        "export_header": "📤 *Your Plant List — {date}*\n\n",
        "export_row": (
            "{i}. *{name}*\n"
            "   💧 {freq} (every {days} days)\n"
            "   📅 Last watered: {last} | Next: {next}"
        ),
        "export_row_note": (
            "{i}. *{name}*\n"
            "   💧 {freq} (every {days} days)\n"
            "   📅 Last watered: {last} | Next: {next}\n"
            "   📝 {note}"
        ),
        "export_footer": "\n\n🌍 Bot has {count} plants in database.",
        "export_empty": "No plants to export yet!",

        # Free text search
        "text_search_hint": (
            "🔍 Did you mean a plant? Try:\n"
            "/search {query}\n\n"
            "Or use /start to browse categories."
        ),

        # Search / plant lookup
        "plant_cmd_usage": "Usage: /plant <name>  or  /search <name>\nOr just type the plant name!",
        "plant_found": (
            "🌿 *{ar_name}* ({en_name})\n"
            "📂 {category}\n\n"
            "💧 *Watering schedule:*\n"
            "   Every *{days}* day(s) — {freq}\n\n"
            "📝 {tips}"
        ),
        "plant_not_found": (
            "❌ *{query}* not found in database.\n\n"
            "Try /start to browse categories\n"
            "Or add manually: /add {query} <days>"
        ),
        "plant_db_count": "🌍 *{count}* plants in database.",
        "search_no_query": (
            "🔍 *Plant Search*\n\n"
            "Usage: /search <plant name>\n"
            "Example: /search rose\n\n"
            "🌍 Database: *{count}* plants across 16 categories.\n"
            "_Or just type the plant name directly!_"
        ),
        "add_from_db_btn": "➕ Add to my plants",
        "added_already_btn": "✅ Added!",
        "add_from_db_success": (
            "✅ *{name}* added!\n\n"
            "💧 Schedule: {freq} (every {days} days)\n"
            "📅 Next watering: *{date}*\n\n"
            "/myplants to see all your plants."
        ),

        # Frequency labels
        "freq_daily": "Daily",
        "freq_xday": "Every {n} days",
        "freq_weekly": "Once/week",
        "freq_twice_week": "Twice/week",
        "freq_twice_month": "Twice/month",
        "freq_monthly": "Once/month",
        "freq_rare": "Every {n} days (drought-tolerant)",
    },

    "ar": {
        "welcome": (
            "🌱 *بوت العناية بالنباتات*\n\n"
            "سأساعدك في تذكر سقي نباتاتك!\n\n"
            "*الأوامر:*\n"
            "/search `<الاسم>` — ابحث في 358+ نبات\n"
            "/myplants — نباتاتك مع جدول السقي\n"
            "/schedule — جدول السقي الأسبوعي\n"
            "/next — أقرب مواعيد السقي\n"
            "/add `<الاسم> <الأيام>` — أضف نباتاً يدوياً\n"
            "/watered `<الرقم>` — تأشير نبات تم سقيه\n"
            "/delete `<الرقم>` — احذف نباتاً\n"
            "/edit `<الرقم> <الأيام>` — غيّر جدول السقي\n"
            "/rename `<الرقم> <الاسم الجديد>` — غيّر اسم نبات\n"
            "/note `<الرقم> <النص>` — أضف ملاحظة\n"
            "/vacation `<الأيام>` — وقف التذكيرات\n"
            "/stats — إحصائيات عنايتك بالنباتات\n"
            "/export — تصدير قائمة نباتاتك\n"
            "/reminder `<الساعة>` — خصص وقت التذكير\n\n"
            "_أو اكتب اسم النبات مباشرة للبحث عنه!_"
        ),
        "language_saved": "✅ تم ضبط اللغة على العربية.",
        "choose_category": "🌿 اختر فئة لتصفح النباتات:",
        "category_plants_header": "{emoji} *{name}*\n\nاختر نباتاً لعرض تفاصيل العناية:",
        "back_categories": "⬅️ العودة للفئات",
        "back_to_plant_list": "⬅️ رجوع للقائمة",

        # Add plant
        "add_usage": "الاستخدام: /add <اسم النبات> <عدد الأيام>\nمثال: /add مونستيرا 7",
        "add_days_error": "الوسيط الأخير يجب أن يكون عدد الأيام.\nمثال: /add مونستيرا 7",
        "add_interval_error": "موعد السقي يجب أن يكون يوماً واحداً على الأقل.",
        "add_success": "✅ تمت إضافة *{name}*\n💧 {freq} (كل {days} يوم)",

        # My plants
        "no_plants": (
            "🌵 لا توجد نباتات بعد.\n\n"
            "تصفح الفئات أعلاه، أو:\n"
            "/add <الاسم> <الأيام>"
        ),
        "plants_header": "🪴 *نباتاتك:*\n",
        "plant_row": "{i}. *{name}*\n   💧 {freq}  |  {status}",
        "plant_row_note": "{i}. *{name}*\n   💧 {freq}  |  {status}\n   📝 {note}",
        "status_overdue": "⚠️ متأخر {n} يوم!",
        "status_today": "💧 اسقه اليوم!",
        "status_ok": "✅ بعد {n} يوم",

        # Watered
        "watered_usage": "الاستخدام: /watered <رقم النبات>\nاستخدم /myplants لرؤية الأرقام",
        "watered_number_error": "يرجى تقديم رقم النبات، مثال: /watered 1",
        "watered_not_found": "النبات رقم {n} غير موجود. لديك {total} نبات.",
        "watered_success": "💧 تم سقي *{name}*! ✅\nالسقي القادم: *{date}*",

        # Delete
        "delete_usage": "الاستخدام: /delete <رقم النبات>\nمثال: /delete 2",
        "delete_confirm": "⚠️ هل تريد حذف *{name}*؟\nلا يمكن التراجع.",
        "delete_yes_btn": "🗑️ نعم، احذفه",
        "delete_no_btn": "❌ إلغاء",
        "delete_success": "🗑️ تم حذف *{name}*.",
        "delete_not_found": "النبات رقم {n} غير موجود.",
        "delete_cancelled": "✅ تم الإلغاء — النبات محفوظ.",

        # Edit
        "edit_usage": "الاستخدام: /edit <الرقم> <الأيام>\nمثال: /edit 1 5",
        "edit_days_error": "الصيغة: /edit <الرقم> <الأيام>\nمثال: /edit 1 10",
        "edit_not_found": "النبات رقم {n} غير موجود. لديك {total} نبات.",
        "edit_success": "✅ تم تحديث *{name}*!\n💧 الجديد: {freq} (كل {days} يوم)",

        # Rename
        "rename_usage": "الاستخدام: /rename <الرقم> <الاسم الجديد>\nمثال: /rename 1 وردتي الحمراء",
        "rename_not_found": "النبات رقم {n} غير موجود.",
        "rename_success": "✅ تم تغيير الاسم إلى *{name}*!",

        # Note
        "note_usage": "الاستخدام: /note <الرقم> <النص>\nمثال: /note 1 بجانب الشباك",
        "note_not_found": "النبات رقم {n} غير موجود.",
        "note_success": "📝 تمت إضافة ملاحظة لـ *{name}*:\n_{note}_",
        "note_cleared": "📝 تم مسح ملاحظة *{name}*.",

        # Vacation
        "vacation_usage": "الاستخدام: /vacation <الأيام>\nمثال: /vacation 7\nاستخدم /vacation 0 للإلغاء.",
        "vacation_set": "🏖️ وضع الإجازة مفعّل لمدة *{days}* يوم.\nالتذكيرات موقوفة حتى *{until}*.",
        "vacation_cancelled": "✅ انتهت الإجازة — التذكيرات استُؤنفت!",
        "vacation_active": "🏖️ وضع الإجازة مفعّل حتى *{until}*.\nاستخدم /vacation 0 للإلغاء.",
        "vacation_days_error": "يرجى تقديم عدد الأيام، مثال: /vacation 7",

        # Schedule
        "schedule_header": "📅 *جدول السقي الأسبوعي:*\n",
        "schedule_today": "📍 اليوم ({day}):",
        "schedule_day": "📅 {day}:",
        "schedule_empty_day": "✅ لا سقي",
        "schedule_no_plants": "لا توجد نباتات بعد! أضف نباتاً بـ /add أو تصفح الفئات.",
        "days_ar": ["الإثنين", "الثلاثاء", "الأربعاء", "الخميس", "الجمعة", "السبت", "الأحد"],

        # Next
        "next_header": "📅 *أقرب مواعيد السقي:*\n",
        "next_today": "💧 اليوم: {names}",
        "next_tomorrow": "📅 غداً: {names}",
        "next_day": "📅 بعد {n} يوم ({day}): {names}",
        "next_all_ok": "✅ جميع النباتات على المسار!\nكل شيء تم سقيه مؤخراً.",
        "next_overdue": "⚠️ متأخرة: {names}",

        # Stats
        "stats_header": "📊 *إحصائيات نباتاتك:*\n",
        "stats_body": (
            "🌱 إجمالي النباتات: *{total}*\n"
            "✅ على المسار: *{ok}*\n"
            "💧 تحتاج سقي اليوم: *{today}*\n"
            "⚠️ متأخرة: *{overdue}*\n\n"
            "💦 مجموع مرات السقي: *{waterings}*\n"
            "🔥 سلسلة السقي: *{streak} يوم متتالي*\n"
            "📅 أقرب موعد سقي: *{next_name}* ({next_days})"
        ),
        "stats_no_next": "جميعها على المسار!",
        "stats_empty": "لا توجد نباتات بعد. أضف نباتاً بـ /add أو تصفح الفئات!",

        # Reminder
        "reminder_usage": "الاستخدام: /reminder <الساعة (0–23)>\nمثال: /reminder 9",
        "reminder_invalid": "يرجى تقديم ساعة صحيحة بين 0 و 23.",
        "reminder_set": "⏰ تم ضبط التذكير على *{hour}:00* كل يوم.",

        # Reminder message
        "reminder_header": "💧 *حان وقت سقي النباتات!*\n",
        "reminder_overdue": "⚠️ *{name}* — متأخر {n} يوم!",
        "reminder_today": "🌱 *{name}* — اسقه اليوم",
        "reminder_footer": "\nاضغط على زر أسفله أو استخدم /watered <الرقم>.",
        "quick_water_btn": "💧 سقيت",
        "quick_water_done": "✅ تم سقي {name}!\nالقادم: {date}",

        # Export
        "export_header": "📤 *قائمة نباتاتك — {date}*\n\n",
        "export_row": (
            "{i}. *{name}*\n"
            "   💧 {freq} (كل {days} يوم)\n"
            "   📅 آخر سقي: {last} | القادم: {next}"
        ),
        "export_row_note": (
            "{i}. *{name}*\n"
            "   💧 {freq} (كل {days} يوم)\n"
            "   📅 آخر سقي: {last} | القادم: {next}\n"
            "   📝 {note}"
        ),
        "export_footer": "\n\n🌍 قاعدة البيانات: {count} نبات.",
        "export_empty": "لا توجد نباتات للتصدير بعد!",

        # Free text search
        "text_search_hint": (
            "🔍 هل تبحث عن نبات؟ جرب:\n"
            "/search {query}\n\n"
            "أو استخدم /start لتصفح الفئات."
        ),

        # Search / plant lookup
        "plant_cmd_usage": "الاستخدام: /plant <اسم النبات>  أو  /search <الاسم>\nأو اكتب الاسم مباشرة!",
        "plant_found": (
            "🌿 *{ar_name}* ({en_name})\n"
            "📂 {category}\n\n"
            "💧 *جدول السقي:*\n"
            "   كل *{days}* يوم — {freq}\n\n"
            "📝 {tips}"
        ),
        "plant_not_found": (
            "❌ *{query}* غير موجود في قاعدة البيانات.\n\n"
            "جرب /start لتصفح الفئات\n"
            "أو أضفه يدوياً: /add {query} <أيام>"
        ),
        "plant_db_count": "🌍 قاعدة البيانات: *{count}* نبات.",
        "search_no_query": (
            "🔍 *بحث النباتات*\n\n"
            "الاستخدام: /search <اسم النبات>\n"
            "مثال: /search ورد\n\n"
            "🌍 قاعدة البيانات: *{count}* نبات في 16 فئة.\n"
            "_أو اكتب اسم النبات مباشرة!_"
        ),
        "add_from_db_btn": "➕ أضف لنباتاتي",
        "added_already_btn": "✅ تمت الإضافة!",
        "add_from_db_success": (
            "✅ تمت إضافة *{name}*!\n\n"
            "💧 جدول السقي: {freq} (كل {days} يوم)\n"
            "📅 السقي القادم: *{date}*\n\n"
            "/myplants لعرض جميع نباتاتك."
        ),

        # Frequency labels
        "freq_daily": "يومياً",
        "freq_xday": "كل {n} أيام",
        "freq_weekly": "مرة في الأسبوع",
        "freq_twice_week": "مرتين في الأسبوع",
        "freq_twice_month": "مرتين في الشهر",
        "freq_monthly": "مرة في الشهر",
        "freq_rare": "كل {n} يوم (يتحمل الجفاف)",
    },
}


def t(lang: str, key: str, **kwargs) -> str:
    text = STRINGS.get(lang, STRINGS["en"]).get(key, STRINGS["en"].get(key, key))
    return text.format(**kwargs) if kwargs else text
