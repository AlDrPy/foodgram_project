import json
import os

from django.core.management.base import BaseCommand

from receipts.models import Ingredient


class Command(BaseCommand):

    help = 'Загрузка ингредиентов в базу '

    path = os.path.abspath('data/ingredients.json')

    def handle(self, *args, **kwargs):
        with open(self.path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        for entry in data:
            try:
                Ingredient.objects.get_or_create(**entry)
                print(f'{entry["name"]} записан в базу')
            except Exception as error:
                print(f'Ошибка при добавлении {entry["name"]} в базу.\n'
                      f'Ошибка: {error}')

        print('Загрузка завершена.')
