import requests, json, config

url = 'https://www.brooklynmuseum.org/api/v2/exhibition/'
headers = {'api_key': config.API_KEY}

def main():
    exhibitions = []
    payload = {'total_count_only': 1}
    num_exhibitions = int(requests.get(url, headers=headers, params=payload).json()['data'])

    # API limits responses to 35 items at a time.
    # While loop fetches the next 35 items and
    # adds each item to a new JSON array until dataset is exhausted.
    while(len(exhibitions) < num_exhibitions):
        payload = {'offset': len(exhibitions), 'limit': 35}
        r = requests.get(url, headers=headers, params=payload)
        print "Fetching: {} records".format(len(r.json()['data']))
        for item in r.json()['data']:
            exhibitions.append(item)
    print "Total records: {}".format(len(exhibitions))
    with open('json/exhibitions.json', 'wb') as f:
        json.dump(exhibitions, f)

if __name__ == '__main__':
    main()
