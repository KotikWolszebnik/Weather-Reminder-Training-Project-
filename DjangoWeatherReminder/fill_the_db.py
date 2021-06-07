from json import load
from os import environ
from os.path import dirname

from django import setup
from django.db.transaction import atomic

environ.setdefault("DJANGO_SETTINGS_MODULE", "DjangoWeatherReminder.settings")
setup()

from api.models import City


@atomic
def fill_the_db():
    file_path = f'{dirname(__file__)}/cities_all.json'

    with open(file_path, 'r') as file_handler:
        cities_list = load(file_handler)

    for city in cities_list:
        obj = City(
            id=city['city_id'],
            name=city['city_name'],
            state_code=city['state_code'],
            country=city['country_full'],
            country_code=city['country_code'],
        )
        obj.save()


if __name__ == "__main__":
    fill_the_db()
