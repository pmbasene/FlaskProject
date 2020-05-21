import requests
from pprint import pprint

cityname = 'London'
yourapikey = '47c070163f772ba63244f399e7be83f2'
units = 'metric'   #imperial

url = f'https://api.openweathermap.org/data/2.5/weather?q={cityname}&appid={yourapikey}&units={units}'

r = requests.get(url)
resp = r.json()

# useful data 
main = resp['main']
temp = resp['main']['temp']
feels_like = resp['main']['feels_like'] 
temp_min = resp['main']['temp_min']
temp_max = resp['main']['temp_max']
pressure = resp['main']['pressure']
humidity = resp['main']['humidity']


weather = resp['weather'] 
description = weather[0]['description'] 
icon = weather[0]['icon'] 

wind_speed =  resp['wind']['speed']
# wind_deg = resp['wind']['deg']


pprint(resp)
# pprint(malsin)
# print(description)
# print(temp)
# print(pressure)
# print(icon)
# print(wind_speed)
# print(wind_deg)
