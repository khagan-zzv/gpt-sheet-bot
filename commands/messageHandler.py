import asyncio
from secrets import authorized_user_id
from telegram import Update
from telegram.ext import ContextTypes
import state
from commands.botCommands import (
    WAITING_PROMPT, WAITING_SHEET_CHANGE, WAITING_SHEET_ID, WAITING_SYSTEM_PROMPT,
    handle_sheet_id, handle_system_prompt
)


from ai_control.ai_control import process_message

async def handle_user_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message.text.strip()

    if update.effective_user.id != authorized_user_id:
        print(update.effective_user.id)
        await update.message.reply_text("🚫 Sorry, this bot is private.")
        return
    if context.user_data.get(WAITING_PROMPT):
        state.system_prompt = message
        context.user_data[WAITING_PROMPT] = False
        await update.message.reply_text("✅ System prompt updated!")
        return

    if context.user_data.get(WAITING_SHEET_CHANGE):
        state.sheetID = message
        context.user_data[WAITING_SHEET_CHANGE] = False
        await update.message.reply_text(f"✅ Sheet ID changed to `{state.sheetID}`", parse_mode="Markdown")
        return

    if context.user_data.get(WAITING_SHEET_ID):
        await handle_sheet_id(update, context, message)
        return

    if context.user_data.get(WAITING_SYSTEM_PROMPT):
        await handle_system_prompt(update, context, message)
        return

    if not state.sheetID:
        await update.message.reply_text("⚠️ Please first set a valid sheet ID with /start or /sheet.")
        return

    # Run AI
    loop = asyncio.get_event_loop()
    ai_response = await loop.run_in_executor(None, process_message, message, state.sheetID)

    if ai_response["success"]:
        await update.message.reply_text(ai_response["data"] or "🤖 (No response generated)")
    else:
        await update.message.reply_text("❌ Error:\n" + ai_response["error"])
