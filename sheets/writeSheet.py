from googleapiclient.errors import HttpError
from auth import get_sheets_service

def write_to_sheet(sheet_id: str, range_str: str, value: str):
    print(f"Writing {value} to {range_str}")
    try:
        service = get_sheets_service()
        body = {
            "values": [[value]]
        }

        service.spreadsheets().values().update(
            spreadsheetId=sheet_id,
            range=range_str,
            valueInputOption="USER_ENTERED",
            body=body
        ).execute()
        print(f"Wrote {value} to {range_str}")
        return f"Updated {range_str} to: {value}"

    except HttpError as err:
        return f"Error updating sheet: {err}"

def write_multiple_to_sheet(sheet_id: str, updates: list[dict]) -> str:
    try:
        service = get_sheets_service()
        data = [{"range": u["range"], "values": [[u["value"]]]} for u in updates]

        body = {
            "valueInputOption": "USER_ENTERED",
            "data": data
        }

        result = service.spreadsheets().values().batchUpdate(
            spreadsheetId=sheet_id,
            body=body
        ).execute()
        print("Updated in batch")
        return f"Updated {len(updates)} cells successfully!"
    except HttpError as err:
        return f"Error: {err}"

