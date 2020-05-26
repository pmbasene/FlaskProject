import requests
def get_weather_data(city):
    """ Cette fonction permet de faire une requete vers l' api openWeather

        Arguments:
            city {[string]} -- le nom de la ville

        Returns:
            [json] -- dataset
    """
    yourapikey = '47c070163f772ba63244f399e7be83f2'
    units = 'metric'  # imperial cityname
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={yourapikey}&units={units}'
    r = requests.get(url)
    return r.json()
