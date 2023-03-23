from oauth2client.service_account import ServiceAccountCredentials
import gspread


def add_patron_to_sheets(email, steam64id):
    scopes = ['https://www.googleapis.com/auth/spreadsheets',
              'https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(".\patreon-sheet.json", scopes)
    file = gspread.authorize(credentials)
    sheet = file.open("Patreon Bot Sheet")
    sheet = sheet.sheet1
    patron = sheet.find(steam64id, in_column=2)
    data = [email, steam64id]
    if patron is None:
        insert_to_sheet(sheet, data)
        return "We have added this patron to the database!"
    return "This patron is already in our database."


def insert_to_sheet(sheet, data, offset=1):
    sheet.insert_row(data, offset)
