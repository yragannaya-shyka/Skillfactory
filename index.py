import requests
import json
base_key = 'RUB'
quote_key = 'USD'
r = requests.get(f"https://min-api.cryptocompare.com/data/price?fsym={base_key}&tsyms={quote_key}")
resp = json.loads(r.content)[quote_key]
print(resp)
