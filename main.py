import json
import requests
import pandas as pd


api_url_base = 'https://api-v3.mbta.com/routes?filter[type]=0,1'
headers = {'Content-Type': 'application/json'}

response = requests.get(api_url_base, headers=headers)

class Routes:
    def __init__(self, long_name, id):
        self.long_name = long_name
        self.id = id
        
    def q1(self):
        print(self.long_name)
        


if response.status_code == 200:
    print('Success!')
    json_resp = response.json()
    tests = json_resp["data"]
    rts = []
    for test in tests:
        id = test['id']
        name = test['attributes']['long_name']
        rts.append(Routes(name, id))
    df_routes = pd.DataFrame(rts)
    for rt in rts:
        rt.q1()
elif response.status_code == 404:
    print('Not Found.')
