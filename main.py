from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from commands.botCommands import set_system_prompt, change_sheet_id, start
from commands.messageHandler import handle_user_message
from secrets import token


BOT_TOKEN = token

if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("prompt", set_system_prompt))
    app.add_handler(CommandHandler("sheet", change_sheet_id))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_user_message))

    print("Bot is running...")
    app.run_polling()
