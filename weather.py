import requests
import json
import datetime


def check_weather():
    snow_times = []
    with open('weather_config.txt', 'r') as f:
        zipcode = f.readline()
        rapidapikey = f.readline()

    url = "https://community-open-weather-map.p.rapidapi.com/forecast"
    querystring = {"units":"standard","zip":zipcode.strip()}

    headers = {
        'x-rapidapi-host': "community-open-weather-map.p.rapidapi.com",
        'x-rapidapi-key': rapidapikey.strip()
        }

    response = requests.request("GET", url, headers=headers, params=querystring)
    response_json = json.loads(response.text)
    for i in response_json['list']:
        if i['weather'][0]['main'] == 'Snow':
            snow_times.append(datetime.datetime.fromtimestamp(int(i['dt'])).isoformat())
    return snow_times



def format_message(snow_list):
    message = ''
    for i in snow_list:
        message = message + i + '\n'

    if message == '':
        message = 'No snow!'
    return message

def post_weather():
    return format_message(check_weather())