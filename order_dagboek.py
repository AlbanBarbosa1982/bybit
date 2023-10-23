from pybit.unified_trading import HTTP
import pandas as pd
import json_normalize
from openpyxl import load_workbook
from openpyxl.utils.dataframe import dataframe_to_rows
import requests

# Maak een sessie aan
session = HTTP(
    testnet=False,
    api_key="",
    api_secret="",
)

# Stel dat 'order_data' je originele data is
data = session.get_closed_pnl(
    category="inverse",
    limit=100,
)

# Maak een DataFrame van de gegevens
df = pd.DataFrame(data['result'])  # Wijziging hier

# Ontvouw geneste kolommen
for col in df.columns:
    if isinstance(df[col][0], dict):
        nested_df = pd.DataFrame(df[col].tolist())
        nested_df.columns = [f"{col}_{nested_col}" for nested_col in nested_df.columns]
        df = pd.concat([df, nested_df], axis=1)
        df = df.drop(columns=[col])

# Huidige kolomnamen
print("Huidige kolomnamen:")
print(df.columns)

# Maak een dictionary met de huidige namen als sleutels en de nieuwe namen als waarden
rename_dict = {
    'symbol': 'Symbool',
    'orderId': 'Order ID',
    'side': 'Transactie Type',
    'qty': 'Hoeveelheid',
    'orderPrice': 'Orderprijs',
    'orderType': 'Ordertype',
    'execType': 'Uitvoeringstype',
    'closedSize': 'Gesloten Grootte',
    'cumEntryValue': 'Cumulatieve Entry Waarde',
    'avgEntryPrice': 'Gemiddelde Entry Prijs',
    'cumExitValue': 'Cumulatieve Exit Waarde',
    'avgExitPrice': 'Gemiddelde Exit Prijs',
    'closedPnl': 'Gesloten PnL',
    'fillCount': 'Vul Telling',
    'leverage': 'Hefboom',
    'list_createdTime': 'Aanmaaktijd',
    'list_updatedTime': 'Bijgewerkte Tijd'
}

# Converteer de tijdskolommen naar een leesbaar formaat voor Excel
df['list_createdTime'] = pd.to_datetime(df['list_createdTime'], unit='ms').dt.strftime('%Y-%m-%d %H:%M:%S')
df['list_updatedTime'] = pd.to_datetime(df['list_updatedTime'], unit='ms').dt.strftime('%Y-%m-%d %H:%M:%S')

# Hernoem de kolommen
df.rename(columns=rename_dict, inplace=True)

# Controleer de nieuwe kolomnamen
print("Nieuwe kolomnamen:")
print(df.columns)

# Schrijf het DataFrame naar een Excel-bestand
df.to_excel('order_dagboek.xlsx', index=False)