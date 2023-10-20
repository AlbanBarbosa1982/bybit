from pybit.unified_trading import HTTP
import requests
import json

# Define the API key and API secret
api_key = "JOUWAPIKEY"
api_secret = "JOUWAPIKEY"

# Create an HTTP session
session = HTTP(
    testnet=False,
    api_key=api_key,
    api_secret=api_secret,
)

coins = ["USDT","BTC","HBAR"]

def get_conversion_rate(coin):
    response = requests.get(f'https://api.coingecko.com/api/v3/simple/price?ids={coin}&vs_currencies=eur')
    return response.json()[coin]['eur']

conversion_rates = {}
total_euro = 0

for coin in coins:
    records = session.get_internal_transfer_records(
        coin=coin,
        limit=100,
    )
    
    # Check if records is a dictionary and contains a 'list' key
    if isinstance(records, dict) and 'list' in records['result']:
        # Assuming 'amount' key in each record dict represents the transferred amount
        total_transferred = sum(float(record['amount']) for record in records['result']['list'])
    else:
        print(f"Unexpected structure for records: {records}")
        continue
    
    # Get the conversion rate for the coin
    if coin == "USDT":
        conversion_rate = get_conversion_rate("tether")
    elif coin == "BTC":
        conversion_rate = get_conversion_rate("bitcoin")
    elif coin == "HBAR":
        conversion_rate = get_conversion_rate("hedera-hashgraph")
    
    # Add the total transferred amount in euros to the total
    total_euro += total_transferred * conversion_rate

print(f"Welk bedrag heb je overgemaakt van je funding account naar je subaccount: {total_euro:.2f} euro")

# Now, use this calculated total_euro as totale_storting_bybit
totale_storting_bybit = total_euro

response = session.get_wallet_balance(accountType="CONTRACT", coin="BTC")
# Extract equity in BTC from the response
equity_btc = float(response['result']['list'][0]['coin'][0]['equity'])

# Fetch current BTC to EUR conversion rate from CoinGecko API
response = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=eur')
data = json.loads(response.text)

# Get the conversion rate
btc_to_eur_rate = data['bitcoin']['eur']

# Calculate equity in EUR
equity_eur = round(equity_btc * btc_to_eur_rate, 2)
PNL = round(equity_eur - totale_storting_bybit, 2)
print(f'Je account in na traden is: {equity_eur} euro')
print(f'Je totale PNL is: {PNL} euro')
