import Adafruit_IO
import requests

ADAFRUIT_IO_USERNAME = 'CjayBalls'
ADAFRUIT_IO_KEY = 'aio_PrHT67qgyYsN2x1Cmq2YqGPKq7lf'
aio = Adafruit_IO.Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

feed_name = 'SensorFeed'  

api_key = "c5edae66c459cb80a6c09d9aacea3e2c"

base_url = "http://api.openweathermap.org/data/2.5/weather?"

city_name = input("City Name: ")

graus = "&units=metric"

full_url = base_url + "appid=" + api_key + "&q=" + city_name + graus
response = requests.get(full_url)
x = response.json()
if x["cod"] != "404":
    y = x["main"]
    current_temperature = y["temp"]
    current_pressure = y["pressure"]
    current_humidity = y["humidity"]
    z = x["weather"]
    weather_description = z[0]["description"]
    aio.send('sensorfeed', current_temperature)
else:
    print("City not found")
