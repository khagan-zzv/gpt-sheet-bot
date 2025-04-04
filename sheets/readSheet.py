from googleapiclient.errors import HttpError
from sheets.auth import get_sheets_service

def read_entire_sheet(sheet_id, sheet_tab=None):
    try:
        service = get_sheets_service()

        # Auto-detect tab name if none is provided
        if not sheet_tab:
            metadata = service.spreadsheets().get(spreadsheetId=sheet_id).execute()
            sheet_tab = metadata["sheets"][0]["properties"]["title"]

        range_str = f"{sheet_tab}!A1:Z50"

        result = service.spreadsheets().values().get(
            spreadsheetId=sheet_id,
            range=range_str
        ).execute()

        values = result.get("values", [])
        if not values:
            return {"success": True, "data": f"📭 '{sheet_tab}' is empty."}

        formatted = []
        for row_idx, row in enumerate(values):
            for col_idx, val in enumerate(row):
                cell = f"{chr(65 + col_idx)}{row_idx + 1}"
                formatted.append(f"Cell {sheet_tab}!{cell}: {val}")
        print(formatted)
        return {"success": True, "data": '\n'.join(formatted)}

    except HttpError as err:
        return {"success": False, "error": str(err)}
