import json
import requests


api_url_base = 'https://api-v3.mbta.com/'
headers = {'Content-Type': 'application/json'}

response = requests.get(api_url_base, headers=headers)

print(response)
