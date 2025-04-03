from googleapiclient.errors import HttpError

from sheets.auth import get_sheets_service


def list_sheet_names(sheet_id: str):
    try:
        service = get_sheets_service()
        metadata = service.spreadsheets().get(spreadsheetId=sheet_id).execute()
        return [sheet["properties"]["title"] for sheet in metadata.get("sheets", [])]
    except HttpError as err:
        return ["Error: " + str(err)]