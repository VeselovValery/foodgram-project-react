from csv import DictReader

from django.core.management import BaseCommand

from recipes.models import Ingredient


class Command(BaseCommand):
    help = 'Load data from .csv files'

    def handle(self,  *args, **kwds):
        print('Loading data from .csv files')
        for row in DictReader(
            open('data/ingredients.csv', encoding="utf-8"),
            fieldnames=['name', 'unit']
        ):
            ingredient = Ingredient(name=row['name'], unit=row['unit'])
            ingredient.save()
        print('ingredients.csv uploaded')
