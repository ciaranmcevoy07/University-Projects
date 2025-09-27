import requests
#https://openweathermap.org/current
api_key = "c5edae66c459cb80a6c09d9aacea3e2c"
#url
base_url = "http://api.openweathermap.org/data/2.5/weather?"
#define the city
city_name = input("City Name: ")
#para vir em graus celsius
graus = "&units=metric"
#formar o url do pedido
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
    print(" Temperature = " +
    str(current_temperature) +
    "\n atmospheric pressure (in hPa unit) = " +
    str(current_pressure) +
    "\n humidity (in percentage) = " +
    str(current_humidity) +
    "\n description = " +
    str(weather_description))
else:
    print("City not found")