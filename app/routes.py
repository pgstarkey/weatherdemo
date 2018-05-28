from app import app
from app.weather import (weather_forecast, full_response, temperature_response,
                         pressure_response, humidity_response)


@app.route('/weather/<place>/<qdate>/<qtime>', methods=['GET'])
def full_forecast(place, qdate, qtime):
    return weather_forecast(place, qdate, qtime, full_response)


@app.route('/weather/<place>/<qdate>/<qtime>/temperature', methods=['GET'])
def temperature_forecast(place, qdate, qtime):
    return weather_forecast(place, qdate, qtime, temperature_response)


@app.route('/weather/<place>/<qdate>/<qtime>/pressure', methods=['GET'])
def pressure_forecast(place, qdate, qtime):
    return weather_forecast(place, qdate, qtime, pressure_response)


@app.route('/weather/<place>/<qdate>/<qtime>/humidity', methods=['GET'])
def humidity_forecast(place, qdate, qtime):
    return weather_forecast(place, qdate, qtime, humidity_response)
