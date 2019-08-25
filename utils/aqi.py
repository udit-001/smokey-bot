import os

import requests

import config

AQI_TOKEN = os.environ.get('aqi_token', config.aqi_token)


def get_details(lat, longt):
    endpoint = 'https://api.waqi.info/feed/geo:{0};{1}/?token={2}'.format(
        lat, longt, AQI_TOKEN)

    r = requests.get(endpoint)
    result = r.json()

    aqi = result['data']['aqi']
    city = result['data']['city']['name']
    url = result['data']['city']['url']
    pol = result['data']['dominentpol']
    attrib = result['data']['attributions']

    attrib_string = ''
    count = 0
    length = len(attrib)
    for item in attrib:
        if count == length - 1:
            attrib_string += '['+item['url'].replace('http://', ' ').replace(
                '/', ' ').strip()+']('+item['url']+').'
        else:
            attrib_string += '['+item['url'].replace('http://', ' ').replace(
                '/', ' ').strip()+']('+item['url']+'), '
        count = count + 1

    classf = classify(aqi)

    message = "*{0}*\nAQI : {1} ({2})\nDominant Pollutant : {3}\nFor more info, click [here.]({4})\n_Source:_ {5}".format(
        city, aqi, classf, pol.upper(), url, attrib_string)

    return message, aqi, pol


def classify(aqi):
    if aqi < 51:
        return "Good"
    elif aqi < 101:
        return "Moderate"
    elif aqi < 151:
        return "Unhealthy for Sensitive Groups"
    elif aqi < 201:
        return "Unhealthy"
    elif aqi < 301:
        return "Very Unhealthy"
    else:
        return "Hazardous"


def search_place(query):
    endpoint = f"https://api.waqi.info/search/?keyword={query}&token={AQI_TOKEN}"

    r = requests.get(endpoint)
    result = r.json()

    output = []

    if len(result['data']) == 0:
        return False
    else:
        for i in range(len(result['data'])):
            lat = result['data'][i]['station']['geo'][0]
            long = result['data'][i]['station']['geo'][1]
            if lat == 0 and long == 0:
                pass
            else:
                place = {
                    'name': result['data'][i]['station']['name'],
                    'lat': lat,
                    'long': long
                }
                output.append(place)
        return output
