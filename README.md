# weatherdemo
Demonstration project for providing weather forecasts from OpemWeatherMap

Requirements:
Python 3.x
Flask
Requests

To run, assuming Flask is istalled within the local virtual environment:
(linux) export FLASK_APP=weather_root.py
(Windows) set FLASK_APP=weather_root.py
flask run

Weather forecasts are provided for up to 6 days in advance (controlled by the max_days parameter in weather.cfg).

Please replace the configured APPID (held as app_id in weather.cfg) with your own APPID before use.
