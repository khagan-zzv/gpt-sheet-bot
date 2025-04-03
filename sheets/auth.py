import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import secrets

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
TOKEN_PATH = "../token.json"
CREDS_PATH = "../credentials.json"

def get_sheets_service():
    creds = None
    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDS_PATH, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_PATH, "w") as token:
            token.write(creds.to_json())
    return build("sheets", "v4", credentials=creds)

def check_sheet_access(sheet_id):
    try:
        service = get_sheets_service()
        sheet_metadata = service.spreadsheets().get(spreadsheetId=sheet_id).execute()
        title = sheet_metadata.get("properties", {}).get("title", "Untitled")
        secrets.sheetID=sheet_id
        return {"success": True, "title": title}
    except HttpError as err:
        return {"success": False, "error": str(err)}
