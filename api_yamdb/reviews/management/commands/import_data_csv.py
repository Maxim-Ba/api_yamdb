from csv import DictReader
from django.core.management import BaseCommand
from django.core.exceptions import ObjectDoesNotExist

from reviews.models import Category, Genre, Review
from reviews.models import Title, User, Comment, TitleGenre


CSV_FILES = [
    'genre.csv',
    'category.csv',
    'comments.csv',
    'titles.csv',
    'genre_title.csv',
    'review.csv',
    'users.csv',
]

SAVED_MESSAGE = 'Данные сохранены'
NOT_SAVED_MESSAGE = 'Данные по внешнему ключу не найдены'


class Command(BaseCommand):
    help = "Загрузка данных из CSV файлов"

    def handle(self, *args, **options):
        for csv_file in CSV_FILES:
            with open(f'./static/data/{csv_file}', encoding='utf-8') as file:
                reader = DictReader(file)
                print(f'Идет загрузка данных из {csv_file}...')
                for row in reader:
                    if csv_file == 'user.csv':
                        UserLoad(row)
                    elif csv_file == 'category.csv':
                        CategoryLoad(row)
                    elif csv_file == 'genre.csv':
                        GenreLoad(row)
                    elif csv_file == 'review.csv':
                        ReviewLoad(row)
                    elif csv_file == 'title.csv':
                        TitleLoad(row)
                    elif csv_file == 'comment.csv':
                        CommentLoad(row)
                    elif csv_file == 'genre_title.csv':
                        GenreTitleLoad(row)


def UserLoad(row):
    user = User(
        id=row['id'],
        username=row['username'],
        email=row['email'],
        role=row['role'],
        bio=row['bio'],
        first_name=row['first_name'],
        last_name=row['last_name']
    )
    user.save()
    print(SAVED_MESSAGE)


def CategoryLoad(row):
    category = Category(
        id=row['id'],
        name=row['name'],
        slug=row['slug']
    )
    category.save()
    print(SAVED_MESSAGE)


def GenreLoad(row):
    genre = Genre(
        id=row['id'],
        name=row['name'],
        slug=row['slug']
    )
    genre.save()
    print(SAVED_MESSAGE)


def ReviewLoad(row):
    try:
        title = Title.objects.get(id=row['title_id'])
        review = Review(
            id=row['id'],
            title=title,
            text=row['text'],
            author=row['author'],
            score=row['score'],
            pub_date=row['pub_date']
        )
        review.save()
        print(SAVED_MESSAGE)
    except ObjectDoesNotExist:
        print(NOT_SAVED_MESSAGE)


def TitleLoad(row):
    try:
        category = Category.objects.get(pk=row['category_id'])
    except ObjectDoesNotExist:
        category = None
    title = Title(
        id=row['id'],
        name=row['name'],
        year=row['year'],
        category=category
    )
    title.save()
    print(SAVED_MESSAGE)


def CommentLoad(row):
    try:
        review = Review.objects.get(id=row['review_id'])
        comment = Comment(
            id=row['id'],
            review=review,
            text=row['text'],
            author=row['author'],
            pub_date=row['pub_date']
        )
        comment.save()
        print(SAVED_MESSAGE)
    except ObjectDoesNotExist:
        print(SAVED_MESSAGE)


def GenreTitleLoad(row):
    try:
        genre = Genre.objects.get(pk=row['genre_id'])
        title = Title.objects.get(pk=row['title_id'])
        titlegenre = TitleGenre(
            id=row['id'],
            title=title,
            genre=genre
        )
        titlegenre.save()
        print(SAVED_MESSAGE)
    except ObjectDoesNotExist:
        print(SAVED_MESSAGE)
