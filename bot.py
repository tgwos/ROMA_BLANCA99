import os
import time
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    WebAppInfo
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes
)

# 🔐 TOKEN
TOKEN = os.getenv("BOT_TOKEN")

# 🌐 URL
LOGO_URL = "https://tgwos.github.io/ROMABLANCA99/video1.MP4"
CATALOG_URL = "https://tgwos.github.io/ROMABLANCA99/"

TELEGRAM_CHANNEL_URL = "https://t.me/+E1yYweMiuCRlYWM8"
INSTAGRAM_URL = "https://www.instagram.com/romablanca_93?igsh=Z2VkMW81OWduYTli&utm_source=qr"
WHATSAPP_URL = "https://wa.me/3508127777"

# 🛡️ ANTI-RAID SETTINGS
RATE_WINDOW_SECONDS = 10          # finestra di controllo
MAX_REQUESTS_PER_WINDOW = 5       # max richieste nella finestra
TEMP_BLOCK_SECONDS = 300          # blocco temporaneo: 5 minuti
START_COOLDOWN_SECONDS = 5        # evita spam su /start

# Memoria temporanea in RAM
user_requests = {}
blocked_users = {}
last_start_usage = {}


# 🔹 Tastiera principale
def main_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📦 Apri Catalogo", web_app=WebAppInfo(url=CATALOG_URL))],
        [InlineKeyboardButton("👥 Canale Telegram", url=TELEGRAM_CHANNEL_URL)],
        [InlineKeyboardButton("📞 Contatti ufficiali", callback_data="contacts")],
        [InlineKeyboardButton("📸 Instagram", url=INSTAGRAM_URL)],
        [InlineKeyboardButton("💬 WhatsApp", url=WHATSAPP_URL)]
    ])


# 🔹 Tastiera indietro
def back_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("⬅️ Indietro", callback_data="back")]
    ])


def _now() -> float:
    return time.time()


def cleanup_user_state(user_id: int):
    now = _now()

    # pulizia richieste vecchie
    if user_id in user_requests:
        user_requests[user_id] = [
            t for t in user_requests[user_id]
            if now - t < RATE_WINDOW_SECONDS
        ]
        if not user_requests[user_id]:
            user_requests.pop(user_id, None)

    # pulizia blocco scaduto
    if user_id in blocked_users and blocked_users[user_id] <= now:
        blocked_users.pop(user_id, None)


async def anti_raid_check(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    user = update.effective_user
    if not user:
        return False

    user_id = user.id
    now = _now()

    cleanup_user_state(user_id)

    # utente temporaneamente bloccato
    if user_id in blocked_users:
        seconds_left = int(blocked_users[user_id] - now)
        if seconds_left < 1:
            seconds_left = 1

        text = (
            "🚫 *Troppi tentativi rilevati*\n\n"
            f"Riprova tra circa {seconds_left} secondi."
        )

        if update.callback_query:
            await update.callback_query.answer("Troppi tentativi. Riprova più tardi.", show_alert=True)
        elif update.message:
            await update.message.reply_text(text, parse_mode="Markdown")

        return False

    # registra richiesta
    user_requests.setdefault(user_id, []).append(now)

    # troppe richieste in poco tempo
    if len(user_requests[user_id]) > MAX_REQUESTS_PER_WINDOW:
        blocked_users[user_id] = now + TEMP_BLOCK_SECONDS

        text = (
            "🚫 *Accesso temporaneamente limitato*\n\n"
            "Hai effettuato troppe richieste in poco tempo.\n"
            "Riprova più tardi."
        )

        if update.callback_query:
            await update.callback_query.answer("Sei stato temporaneamente limitato.", show_alert=True)
        elif update.message:
            await update.message.reply_text(text, parse_mode="Markdown")

        return False

    return True


async def start_cooldown_check(update: Update) -> bool:
    user = update.effective_user
    if not user or not update.message:
        return False

    user_id = user.id
    now = _now()
    last_used = last_start_usage.get(user_id, 0)

    if now - last_used < START_COOLDOWN_SECONDS:
        await update.message.reply_text(
            "⏳ Aspetta qualche secondo prima di usare di nuovo /start."
        )
        return False

    last_start_usage[user_id] = now
    return True


# 🔹 /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await anti_raid_check(update, context):
        return

    if not await start_cooldown_check(update):
        return

    await update.message.reply_video(
        video=LOGO_URL,
        caption=(
            "🥇 *BENVENUTO SU ROMA BLANCA93* 🥇\n\n"
            "Il tuo punto di riferimento ufficiale.\n"
            "Accedi al catalogo tramite il pulsante qui sotto.\n\n"
            "📸 Seguimi su Instagram per aggiornamenti continui."
        ),
        parse_mode="Markdown",
        reply_markup=main_keyboard()
    )


# 🔹 Gestione pulsanti
async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if not query:
        return

    if not await anti_raid_check(update, context):
        return

    await query.answer()

    if query.data == "contacts":
        await query.edit_message_caption(
            caption=(
                "📱 *CONTATTI UFFICIALI*\n\n"
                "✈️ *TELEGRAM 1*\n"
                "@rafacaroquintero93\n\n"
                "✈️ *TELEGRAM 2*\n"
                "@arellanofelix93\n\n"
                "📶 *SIGNAL*\n"
                "https://signal.me/#eu/lfrpkpj9BrTOhFWbb0--THMOz_7GZBbUpTA2Fa7BBO_RWUOEM6ZLOJAsJmZso-MD"
            ),
            reply_markup=back_keyboard(),
            parse_mode="Markdown"
        )

    elif query.data == "back":
        await query.edit_message_caption(
            caption=(
                "🥇 *BENVENUTO SU ROMA BLANCA93* 🥇\n\n"
                "Il tuo punto di riferimento ufficiale.\n"
                "Accedi al catalogo tramite il pulsante qui sotto.\n\n"
                "📸 Seguimi su Instagram per aggiornamenti continui."
            ),
            parse_mode="Markdown",
            reply_markup=main_keyboard()
        )


# 🔹 Avvio bot
def main():
    if not TOKEN:
        raise RuntimeError("BOT_TOKEN non impostato")

    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(buttons))

    print("✅ Bot avviato")
    app.run_polling()


# ✅ QUESTO FA PARTIRE IL BOT
if __name__ == "__main__":
    main()
