import json
import openai

from tools import function_tools
from sheets.readSheet import read_entire_sheet
from secrets import open_ai_key, sheetID
from sheets.writeSheet import write_to_sheet, write_multiple_to_sheet
from sheets.findCell import find_cell
from sheets.getSheets import list_sheet_names

openai.api_key = open_ai_key

chat_history = []
MAX_HISTORY = 10
tools=function_tools


def process_message(message, sheet_id):
    try:
        global chat_history

        sheet = sheetID or sheet_id
        result = read_entire_sheet(sheet)
        sheet_context = result["data"] if result["success"] else "Sheet failed to load."

        sheet_tabs = list_sheet_names(sheet)
        sheet_list_text = ", ".join(sheet_tabs)

        system_message = {
            "role": "developer",
            "content": (
                "You are an AI Gym Training assistant helping manage a workout spreadsheet.\n"
                "The user may ask to view or change their workout.\n"
                "You have access to the following tools:\n"
                "1. get_sheet_data: View the sheet content.\n"
                "2. find_cell: Locate a specific value.\n"
                "3. write_to_sheet: Update one cell.\n"
                "4. write_multiple_to_sheet: Update multiple cells in one go.\n"
                "5. list_sheets: Get the list of sheet tabs.\n"
                f"\nAvailable sheet tabs: {sheet_list_text}\n"
                f"\nCurrent sheet content:\n{sheet_context}\n"
                "\nAlways find the correct cell and sheet before writing!"
            )
        }

        chat_history.append({"role": "user", "content": message})
        if len(chat_history) > MAX_HISTORY:
            chat_history = chat_history[-MAX_HISTORY:]

        input_messages = [system_message] + chat_history.copy()

        while True:
            response = openai.responses.create(
                model="gpt-4o",
                input=input_messages,
                tools=tools,
                tool_choice="auto"
            )

            tool_calls = response.output
            function_called = False

            for msg in tool_calls:
                if msg.type == "function_call":
                    function_called = True
                    args = json.loads(msg.arguments)
                    name = msg.name

                    if name == "get_sheet_data":
                        result_obj = read_entire_sheet(args.get("sheet_id") or sheetID)
                        result = result_obj["data"] if result_obj["success"] else f"Error: {result_obj['error']}"
                    elif name == "write_to_sheet":
                        result = write_to_sheet(
                            sheet_id=args.get("sheet_id") or sheetID,
                            range_str=args["range_str"],
                            value=args["value"]
                        )
                    elif name == "write_multiple_to_sheet":
                        result = write_multiple_to_sheet(
                            sheet_id=args.get("sheet_id") or sheetID,
                            updates=args["updates"]
                        )
                    elif name == "find_cell":
                        result = find_cell(
                            sheet_data=args["sheet_data"],
                            search_for=args["search_for"]
                        )
                    elif name == "list_sheets":
                        result = list_sheet_names(args.get("sheet_id") or sheetID)
                        result = ", ".join(result) if isinstance(result, list) else result
                    else:
                        result = f"Unknown tool: {name}"

                    input_messages.append(msg)
                    input_messages.append({
                        "type": "function_call_output",
                        "call_id": msg.call_id,
                        "output": result
                    })
                    break

            if not function_called:
                if response.output_text:
                    chat_history.append({"role": "assistant", "content": response.output_text})
                    if len(chat_history) > MAX_HISTORY:
                        chat_history = chat_history[-MAX_HISTORY:]
                return {"success": True, "data": response.output_text or "🤖 (No response generated)"}

    except Exception as e:
        return {"success": False, "error": str(e)}