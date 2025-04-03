import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import secrets
from ai_control import process_message
from auth import check_sheet_access
from secrets import token

BOT_TOKEN = token

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    await update.message.reply_text(
        "Hey there! 👋\n"
        "Welcome to your online coach! 🏋️‍♂️\n\n"
        "Please send me your *Google Sheet ID* 📄"
        "\n(You can get it from the URL between `/d/` and `/edit`)",
        parse_mode="Markdown"
    )
    context.user_data["expecting_sheet_id"] = True

async def handle_user_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message.text.strip()
    if context.user_data.get("expecting_sheet_id"):
        result = check_sheet_access(message)
        if result["success"]:
            context.user_data["sheet_id"] = message
            context.user_data["expecting_sheet_id"] = False
            await update.message.reply_text(
                f"Access granted to sheet: *{result['title']}*\n\n"
                "Now send a message and I’ll use AI to process it!",
                parse_mode="Markdown"
            )
        else:
            await update.message.reply_text("Couldn't access the sheet. Error:\n" + result["error"])
        return

    if "sheet_id" not in context.user_data:
        await update.message.reply_text("Please first send a valid Sheet ID via /start")
        return
    secrets.sheetID = context.user_data["sheet_id"]

    loop = asyncio.get_event_loop()
    ai_response = await loop.run_in_executor(None, process_message, message, secrets.sheetID)

    if ai_response["success"]:
        response_text = ai_response["data"] or "(No response generated)"
        await update.message.reply_text(response_text)
    else:
        await update.message.reply_text("Error:\n" + ai_response["error"])


if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_user_message))

    print("Bot is running...")
    app.run_polling()
