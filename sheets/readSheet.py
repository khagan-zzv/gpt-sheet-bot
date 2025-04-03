from googleapiclient.errors import HttpError
from auth import get_sheets_service

def read_entire_sheet(sheet_id):
    try:
        service = get_sheets_service()
        metadata = service.spreadsheets().get(spreadsheetId=sheet_id).execute()
        sheet_name = metadata["sheets"][0]["properties"]["title"]
        range_str = f"{sheet_name}!A1:Z50"

        result = service.spreadsheets().values().get(
            spreadsheetId=sheet_id,
            range=range_str
        ).execute()

        values = result.get("values", [])

        if not values:
            return {"success": True, "data": "📭 Sheet is empty."}

        formatted = []
        for row_idx, row in enumerate(values):
            for col_idx, val in enumerate(row):
                cell = f"{chr(65 + col_idx)}{row_idx + 1}"
                formatted.append(f"Cell {cell}: {val}")

        return {"success": True, "data": '\\n'.join(formatted)}

    except HttpError as err:
        return {"success": False, "error": str(err)}
