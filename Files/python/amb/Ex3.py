import requests
base_url = "https://api.openaq.org/v2/locations?"
city_name = input("City Name: ")
full_url = base_url + "city=" + city_name
response = requests.get(full_url)
data = response.json()
for y in data["results"]:
    print('Sensor ID: ', y['id'])
    for parameter in y['parameters']:
        print(parameter['parameter'], parameter['lastValue'])