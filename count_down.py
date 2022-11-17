import requests
import json

request = "https://christmas-days.anvil.app/_/api/get_days"
response = requests.get(request).json()
#print(response)
days_left = response['Days to Christmas']

statement = print(f"{days_left} days left till Christmas")