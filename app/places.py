from json import load


def load_uk():
    """
    Load the places (names, IDs) that OpenWeatherMap supports for the UK.
    :return: dictionary of name: id pairs for UK places supported by
    OpenWeatherMap.  Place names are converted to lower case.
    """
    with open('city.list.json', 'r', encoding='utf8') as json_file:
        all_places = load(json_file)
        return {place['name'].lower(): place['id'] for place in all_places
                if place['country'] == 'GB'}
