import os
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

TELEGRAM_CHANNEL_URL = "https://t.me/+m3wfL3o3jQ4xZTY0"
INSTAGRAM_URL = "https://www.instagram.com/romablanca.93"
WHATSAPP_URL = "https://wa.me/3508797679"
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

# 🔹 /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
    await query.answer()

    if query.data == "contacts":
        await query.edit_message_caption(
            caption=(
                "📱 *CONTATTI UFFICIALI*\n\n"
                "✈️ *TELEGRAM 1*\n"
                "@ragacaroquintero93\n\n"
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
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(buttons))
    app.run_polling()

# ✅ QUESTO FA PARTIRE IL BOT
if __name__== "__main__":
    main()
