import requests
import json


def api_co2():

    distance = 100
    km = distance * 1.852

    f = f"https://despouy.ca/flight-fuel-api/q/?aircraft=60006b&distance={km}"
    response = requests.get(f).json()
    print(response[0]['co2'] )


api_co2()
