import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

creds = ServiceAccountCredentials.from_json_keyfile_name(
    "credentials.json", scope
)

client = gspread.authorize(creds)

def get_sheet_data(sheet_name):
    sheet = client.open("DroneOperations").worksheet(sheet_name)
    data = sheet.get_all_records()
    return pd.DataFrame(data)

def update_pilot_status(pilot_name, new_status):
    sheet = client.open("DroneOperations").worksheet("Pilot_Roster")
    cell = sheet.find(pilot_name)
    sheet.update_cell(cell.row, 8, new_status)  # assume status column is 8
