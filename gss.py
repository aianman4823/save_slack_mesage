from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
import os
from dotenv import load_dotenv

load_dotenv()

SERVICE_ACCOUNT_FILE = os.getenv("SERVICE_ACCOUNT_FILE")
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

credentials = Credentials.from_service_account_file(
    os.path.basename(SERVICE_ACCOUNT_FILE), scopes=SCOPES
)


def import_to_gss(data: list[str]):
    service = build("sheets", "v4", credentials=credentials)

    spreadsheet_id = "1zLxrIJ7lQrRyc1DFBxjw6uUxQgfAOGQqRUxyWlCD9iQ"
    range_name = "シート1"  # データを追加したいシート名

    # 既存のデータの行数を特定
    # result = (
    #     service.spreadsheets()
    #     .values()
    #     .get(spreadsheetId=spreadsheet_id, range=f"{range_name}!A1:A")
    #     .execute()
    # )
    # values = result.get("values", [])
    # last_row = len(values)
    first_row = 1

    request = (
        service.spreadsheets()
        .values()
        .append(
            spreadsheetId=spreadsheet_id,
            range=f"{range_name}!A{first_row + 1}",  # 空いている最初の行からデータを追加
            valueInputOption="USER_ENTERED",
            body={"values": data},
        )
    )

    response = request.execute()
    return response
