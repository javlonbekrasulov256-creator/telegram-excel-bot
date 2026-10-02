import os
import asyncio
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
DELAY = 0.4
MAX_ROWS = 200

if not TOKEN:
    raise RuntimeError("TELEGRAM_BOT_TOKEN topilmadi. .env faylga tokenni kiriting.")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Excel'dagi qatorlarni belgilang → Ctrl+C → shu botga Ctrl+V qilib yuboring.\n"
        "Men har bir bo'sh bo'lmagan qatorni alohida xabar qilib yuboraman."
    )


async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Masalan Excel B2:B11 ni belgilang, Ctrl+C qiling va shu chatga Ctrl+V qilib yuboring."
    )


async def split_rows(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text or ""
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    rows = [row.strip() for row in text.split("\n") if row.strip()]

    if not rows:
        await update.message.reply_text("Bo'sh ma'lumot keldi.")
        return

    if len(rows) == 1:
        await update.message.reply_text(
            "Faqat 1 ta qator keldi. Excel'dan bir nechta qatorni birdan nusxalab yuboring."
        )
        return

    if len(rows) > MAX_ROWS:
        await update.message.reply_text(
            f"Bir martada maksimum {MAX_ROWS} ta qator. Sizda {len(rows)} ta."
        )
        return

    for row in rows:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=row,
            disable_web_page_preview=True
        )
        await asyncio.sleep(DELAY)


def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, split_rows))
    print("Bot ishga tushdi. To'xtatish uchun Ctrl+C.")
    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
