import requests, json, config

url = 'https://www.brooklynmuseum.org/api/v2/object/'
headers = {'api_key': config.API_KEY}

def main():
    objects = []
    payload = {'total_count_only': 1}
    num_objects = int(requests.get(url, headers=headers, params=payload).json()['data'])

    # API limits responses to 35 items at a time.
    # While loop fetches the next 35 items and
    # adds each item to a new JSON array until dataset is exhausted.
    while(len(objects) < num_objects):
        payload = {'offset': len(objects), 'limit': 35}
        r = requests.get(url, headers=headers, params=payload)
        print "Fetching: {} records".format(len(r.json()['data']))
        for item in r.json()['data']:
            objects.append(item)
    print "Total records: {}".format(len(objects))
    with open('json/objects.json', 'wb') as f:
        json.dump(objects, f)

if __name__ == '__main__':
    main()
