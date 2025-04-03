from telegram import Update
from telegram.ext import ContextTypes
import state
from sheets.auth import check_sheet_access

WAITING_SHEET_ID = "expecting_sheet_id"
WAITING_PROMPT = "expecting_prompt"
WAITING_SHEET_CHANGE = "expecting_sheet_id_change"
WAITING_SYSTEM_PROMPT = "expecting_system_prompt"

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    context.user_data[WAITING_SHEET_ID] = True
    await update.message.reply_text(
        "Hey there! 👋 Please send your *Google Sheet ID* 📄",
        parse_mode="Markdown"
    )

# /sheet command
async def change_sheet_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data[WAITING_SHEET_CHANGE] = True
    await update.message.reply_text("📄 Send new Google Sheet ID.")

# /prompt command
async def set_system_prompt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data[WAITING_PROMPT] = True
    await update.message.reply_text("✍️ Send new system prompt.")

# Handle user input for /start sheet
async def handle_sheet_id(update: Update, context: ContextTypes.DEFAULT_TYPE, message: str):
    result = check_sheet_access(message)
    if not result["success"]:
        await update.message.reply_text("❌ Couldn't access the sheet. Error:\n" + result["error"])
        return

    context.user_data[WAITING_SHEET_ID] = False
    context.user_data["sheet_id"] = message
    context.user_data[WAITING_SYSTEM_PROMPT] = True
    state.sheetID = message

    await update.message.reply_text(
        f"✅ Access granted: *{result['title']}*\n\n"
        "Now send your system instructions (one message).",
        parse_mode="Markdown"
    )

# Handle user input for prompt
async def handle_system_prompt(update: Update, context: ContextTypes.DEFAULT_TYPE, message: str):
    state.system_prompt = message
    context.user_data[WAITING_SYSTEM_PROMPT] = False
    await update.message.reply_text("✅ System prompt saved. You're ready to chat!")
