from application import db
from application.apiWeather.utils import get_weather_data
from flask import render_template, url_for, flash, redirect, request, Blueprint
from application.models import Weather
from flask_login import login_user, current_user

weathers = Blueprint('weathers', __name__)



@weathers.route('/apiWeather', methods=['GET'])
def apiWeather():
    #    # todo
    # add city name in data database for query throught a search bar
    # create column side which contains all regions
    
    collectData = []

        
    cities = Weather.query.order_by(Weather.date_posted.desc()).all()

    for city in cities:
        resp = get_weather_data(city.name)
        data = {
                'city': city.name,
                'temp': resp['main']['temp'],
                'temp_min': resp['main']['temp_min'],
                'temp_max': resp['main']['temp_max'],
                'pressure': resp['main']['pressure'],
                'humidity': resp['main']['humidity'],
                'description': resp['weather'][0]['description'],
                'icon': resp['weather'][0]['icon'],
                'wind_speed':  resp['wind']['speed'],
                # 'wind_deg'    : resp['wind']['deg'],
            }
        collectData.append(data)
    return render_template('docEssai/apiWeather.html', collectData=collectData)


@weathers.route('/apiWeather', methods=['POST'])
def apiWeather_post():
    city = request.form.get('city')
    if city:  # check if input , permet d"empecher d'entrer des donnees vides
        check_existing_city = Weather.query.filter_by(name=city).first()
        if not check_existing_city:  # si la ville n'hesite pas deja dans la db. il permet d'eviter la replication
            # on appelle la fonction renvoie le dataset originel de openweather
            resp = get_weather_data(city)
            if resp['cod'] == 200:
                weather = Weather(name=city)
                db.session.add(weather)
                db.session.commit()
            
                flash( f'Good! Les conditions climatiques pour la ville de {city} sont bien disponibles', 'is-success')
            else:
                flash('city not found', 'is-danger')
        else:
            flash("This city already exist in database", "is-danger")
    return redirect(url_for('weathers.apiWeather'))




@weathers.route('/apiWeather/delete/<name>')
def apiWeather_delete_post(name):
    city = Weather.query.filter_by(name=name).first()
    db.session.delete(city)
    db.session.commit()
    flash(f"{name} supprimée ", "is-success")  # ou city.namr
    return redirect(url_for('weathers.apiWeather'))
