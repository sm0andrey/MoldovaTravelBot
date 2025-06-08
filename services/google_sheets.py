from gspread import Client, Spreadsheet, Worksheet, service_account
import aiogram
from asyncio import Lock
from config.google_settings import google_config
from config.table_settings import table_config
lock=Lock()

def client_init_json(file) -> Client:
    """Создание клиента для работы с Google Sheets."""
    return service_account(filename=file)
table_id=table_config.table_id

def get_table_by_id(client: Client, table_url):
    """Получение таблицы из Google Sheets по ID таблицы."""
    return client.open_by_key(table_url)

client = client_init_json(google_config.google_id)
table = get_table_by_id(client, table_id)
async def add_data(client, table, title, data):
    worksheet = table.worksheet(title)
    worksheet.append_row(data)
#add_data(client,table,'requests', ['user_id', 'date', 'city', 'sights'])
def extract_data(table: Spreadsheet, sheet_name: str,row) -> list[dict]:
    """
    Извлекает данные из указанного листа таблицы Google Sheets и возвращает список словарей.

    :param table: Объект таблицы Google Sheets (Spreadsheet).
    :param sheet_name: Название листа в таблице.
    :return: Список словарей, представляющих данные из таблицы.
    """
    worksheet = table.worksheet(sheet_name)
    headers = worksheet.row_values(1)  # Первая строка считается заголовками

    data = []
    rows = worksheet.get_all_values()[1:]  # Начинаем считывать с второй строки

    rows[row] = {headers[i]: value for i, value in enumerate(rows[row])}
    data=rows[row]

    return data