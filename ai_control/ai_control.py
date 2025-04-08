import json
import openai

import state
from ai_control.function_tools import function_tools
from sheets.readSheet import read_entire_sheet
from secrets import open_ai_key
from state import sheetID, chat_history
from sheets.writeSheet import write_to_sheet, write_multiple_to_sheet
from sheets.listSheets import list_sheet_names

openai.api_key = open_ai_key
tools = function_tools


def process_message(message, sheet_id):
    try:

        sheet = sheetID or sheet_id
        result = read_entire_sheet(sheet)
        sheet_context = result["data"] if result["success"] else "Sheet failed to load."

        sheet_tabs = list_sheet_names(sheet)
        sheet_list_text = ", ".join(sheet_tabs)
        print(sheet_list_text)
        print(state.system_prompt)

        system_message = {
            "role": "developer",
            "content": (
                    state.system_prompt + "\n\n"
                                          "You are managing a Google Sheet with multiple tabs (pages).\n"
                                          "You have access to the following tools:\n"
                                          "1. list_sheets: Get available sheet tab names.\n"
                                          "2. get_sheet_data: Read contents from a specific tab.\n"
                                          "3. write_to_sheet: Update a single cell.\n"
                                          "4. write_multiple_to_sheet: Update multiple cells in one go.\n"
                                          f"Sheet ID you are working with: {sheet}\n"
                                          f"Available tabs in this sheet: {sheet_list_text}\n"
                                          f"\nCurrent tab content:\n{sheet_context}\n\n"
                                          "⚠️ IMPORTANT: Always determine the correct tab name before reading or writing.\n"
                                          "- Use `list_sheets` to find tab names.\n"
                                          "- Always call `get_sheet_data` to get the exact cell reference before writing.\n"
            )

        }

        state.chat_history.append({"role": "user", "content": message})
        if len(state.chat_history) > state.MAX_HISTORY:
            chat_history = state.chat_history[-state.MAX_HISTORY:]

        input_messages = [system_message] + state.chat_history.copy()

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
                        sheet_id = args.get("sheet_id") or sheetID
                        sheet_tab = args.get("sheet_tab")
                        result_obj = read_entire_sheet(sheet_id, sheet_tab)
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
                    state.chat_history.append({"role": "assistant", "content": response.output_text})
                    if len(state.chat_history) > state.MAX_HISTORY:
                        state.chat_history = state.chat_history[-state.MAX_HISTORY:]
                return {"success": True, "data": response.output_text or "🤖 (No response generated)"}

    except Exception as e:
        return {"success": False, "error": str(e)}
