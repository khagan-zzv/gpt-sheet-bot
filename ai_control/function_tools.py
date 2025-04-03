function_tools = [
    {
        "type": "function",
        "name": "get_sheet_data",
        "description": "Fetch the full workout sheet for the user.",
        "parameters": {
            "type": "object",
            "properties": {
                "sheet_id": {
                    "type": "string",
                    "description": "Google Sheet ID"
                }
            },
            "required": ["sheet_id"],
            "additionalProperties": False
        },
        "strict": True
    },
    {
        "type": "function",
        "name": "write_to_sheet",
        "description": (
            "Use this function to change or update any value in the user's workout sheet. "
            "For example, if the user wants to replace 'Squats' with 'Lunges' or change a day's plan, "
            "use this function to overwrite that specific cell."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "sheet_id": {"type": "string"},
                "range_str": {"type": "string"},
                "value": {"type": "string"}
            },
            "required": ["sheet_id", "range_str", "value"],
            "additionalProperties": False
        },
        "strict": True
    },
    {
        "type": "function",
        "name": "write_multiple_to_sheet",
        "description": "Batch update multiple cells in the user's workout sheet.",
        "parameters": {
            "type": "object",
            "properties": {
                "sheet_id": {"type": "string"},
                "updates": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "range": {"type": "string"},
                            "value": {"type": "string"}
                        },
                        "required": ["range", "value"],
                        "additionalProperties": False
                    }
                }
            },
            "required": ["sheet_id", "updates"],
            "additionalProperties": False
        },
        "strict": True
    },
    {
        "type": "function",
        "name": "find_cell",
        "description": "Search the sheet and return the cell address where a given keyword exists.",
        "parameters": {
            "type": "object",
            "properties": {
                "sheet_data": {"type": "string"},
                "search_for": {"type": "string"}
            },
            "required": ["sheet_data", "search_for"],
            "additionalProperties": False
        },
        "strict": True
    },
    {
        "type": "function",
        "name": "list_sheets",
        "description": "Return a list of sheet/tab names inside the Google Spreadsheet.",
        "parameters": {
            "type": "object",
            "properties": {
                "sheet_id": {
                    "type": "string",
                    "description": "Google Sheet ID"
                }
            },
            "required": ["sheet_id"],
            "additionalProperties": False
        },
        "strict": True
    }
]