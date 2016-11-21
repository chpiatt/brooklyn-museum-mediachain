import requests, json, config

url = 'https://www.brooklynmuseum.org/api/v2/artist/'
headers = {'api_key':config.API_KEY}

def main():
    artists = []
    payload = {'total_count_only': 1}
    num_artists = int(requests.get(url, headers=headers, params=payload).json()['data'])

    # API limits responses to 35 items at a time.
    # While loop fetches the next 35 items and
    # adds each item to a new JSON array until dataset is exhausted.
    while(len(artists) < num_artists):
        payload = {'offset': len(artists), 'limit': 35}
        r = requests.get(url, headers=headers, params=payload)
        for item in r.json()['data']:
            artists.append(item)
    with open('json/artists.json', 'wb') as f:
        json.dump(artists, f)

if __name__ == '__main__':
    main()
