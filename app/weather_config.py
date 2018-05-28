import configparser

parser = configparser.ConfigParser()
parser.optionxform = str
parser.read('weather.cfg')

base_url = parser.get('Endpoint', 'base_url')
app_id = parser.get('Endpoint', 'app_id')
max_days = int(parser.get('Options', 'max_days'))
