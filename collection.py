import requests, json, config

url = 'https://www.brooklynmuseum.org/api/v2/collection/'
headers = {'api_key': config.API_KEY}

def main():
    collections = []
    # API limits responses to 35 items at a time.
    # While loop fetches the next 35 items and
    # adds each item to a new JSON array until dataset is exhausted.
    r = requests.get(url, headers=headers)
    if len(r.json()['data']) > 0:
        print "Fetching: {} records".format(len(r.json()['data']))
        for item in r.json()['data']:
            collections.append(item)
    print "Total records: {}".format(len(collections))
    with open('json/collections.json', 'wb') as f:
        json.dump(collections, f)

if __name__ == '__main__':
    main()
