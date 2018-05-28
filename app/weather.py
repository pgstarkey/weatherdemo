from datetime import datetime
import json
import math

from flask import request
import requests

import app.weather_config as config
import app.places as places


KELVIN_OFFSET = 273.15
uk_places = places.load_uk()


def weather_forecast(place, qdate, qtime, required_response):
    """
    Return the weather forecast for the specified place that is closest to the
    specified query date and time, giving the response in the required format.
    Error messages are returned if:
    - the query date and time do not form a valid date/time
    - there is no forecast for the specified date/time
    - there is no forecast for the specified place
    :param place: the place for which the forecast is required
    :param qdate: the date (YYYYMMDD) to use for the query
    :param qtime: the time (HHMM) to use for the query
    :param required_response: a function that generates the response in a
    specific format
    :return: the weather forecast, formatted as requested, in JSON format, or
    an error message in JSON format if the forecast cannot be returned
    """
    now = datetime.now()
    try:
        query_time = datetime.strptime(qdate + qtime, '%Y%m%d%H%M')
    except ValueError:
        msg = ' '.join([_datetime_string(qdate, qtime),
                        'is not a valid date/time'])
        return json.dumps({'status': 'error', 'message': msg})
    if place.lower() not in uk_places:
        msg = ' '.join([place, 'is not a valid location'])
        return json.dumps({'status': 'error', 'message': msg})
    if 0 <= (query_time - now).days <= config.max_days:
        forecast = _nearest_forecast(_get_forecast(place.lower()), query_time)
        return json.dumps(required_response(forecast))
    else:
        msg = ' '.join(['No data for', _datetime_string(qdate, qtime)])
        return json.dumps({'status': 'error', 'message': msg})


def full_response(forecast):
    """
    Format the weather forecast in "full" form, including description,
    temperature, pressure and humidity.
    :param forecast: the raw forecast as returned from the backend server
    :return: the forecast in "full" form
    """
    return {'description': forecast['weather'][0]['description'],
            'temperature': _format_temperature(forecast['main']['temp'],
                                               request.args),
            'pressure':  forecast['main']['pressure'],
            'humidity': ''.join([str(forecast['main']['humidity']), '%'])}


def temperature_response(forecast):
    """
    Format the weather forecast so that only temperature is returned.
    :param forecast: the raw forecast as returned from the backend server
    :return: the temperature forecast
    """
    return {'temperature': _format_temperature(forecast['main']['temp'],
                                               request.args)}


def pressure_response(forecast):
    """
    Format the weather forecast so that only pressure is returned.
    :param forecast: the raw forecast as returned from the backend server
    :return: the pressure forecast
    """
    return {'pressure': forecast['main']['pressure']}


def humidity_response(forecast):
    """
    Format the weather forecast so that only humidity is returned.
    :param forecast: the raw forecast as returned from the backend server
    :return: the humidity forecast
    """
    return {'humidity': ''.join([str(forecast['main']['humidity']), '%'])}


# Functions for querying the forecast

def _get_forecast(place):
    payload = {'id': str(uk_places[place]), 'APPID': config.app_id}
    response = requests.get(config.base_url, params=payload)
    response_body = response.json()
    return [entry for entry in response_body['list']]


def _nearest_forecast(forecast, query_time):
    return sorted(
        forecast, key=lambda x: _datetime_offset(x['dt_txt'], query_time))[0]


# Utility functions

def _datetime_string(indate, intime):
    return ' '.join(['-'.join([indate[:4], indate[4:6], indate[6:]]),
                     ':'.join([intime[:2], intime[2:]])])


def _datetime_offset(datetime_iso, ref_datetime):
    return abs(datetime.strptime(
        datetime_iso, '%Y-%m-%d %H:%M:%S') - ref_datetime)


def _format_temperature(temperature, request_args):
    if 'temp' in request_args and request_args['temp'] == 'K':
        return ''.join([str(int(math.ceil(temperature))), 'K'])
    else:
        return ''.join([str(int(math.ceil(temperature - KELVIN_OFFSET))), 'C'])
