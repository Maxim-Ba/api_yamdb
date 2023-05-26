from django.core.management import BaseCommand
from csv import DictReader

from reviews.models import (
    Genre,
)


class Command(BaseCommand):
    help = "Загрузка данных из genre.csv"

    def handle(self, *args, **options):
        for row in DictReader(
            open('./static/data/genre.csv')
        ):
            genre = Genre(id=row['id'], name=row['name'], slug=row['slug'])
            if not Genre.objects.filter(
                name=genre['name'],
                slug=genre['slug']
            ).exists():
                genre.save()
            else:
                print('Данные об этом жанре уже добавлены')