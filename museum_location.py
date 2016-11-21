import requests, json, config

url = 'https://www.brooklynmuseum.org/api/v2/museum-location/'
headers = {'api_key': config.API_KEY}

def main():
    museum_locations = []
    dataExists = True
    # API limits responses to 35 items at a time.
    # While loop fetches the next 35 items and
    # adds each item to a new JSON array until dataset is exhausted.
    while(dataExists):
        payload = {'offset': len(museum_locations), 'limit': 35}
        r = requests.get(url, headers=headers, params=payload)
        if len(r.json()['data']) > 0:
            print "Fetching: {} records".format(len(r.json()['data']))
            for item in r.json()['data']:
                museum_locations.append(item)
        else:
            dataExists = False
    print "Total records: {}".format(len(museum_locations))
    with open('json/museum_locations.json', 'wb') as f:
        json.dump(museum_locations, f)

if __name__ == '__main__':
    main()
