from csv import DictReader
from django.core.management import BaseCommand
from django.core.exceptions import ObjectDoesNotExist

from reviews.models import Category, Genre, Review
from reviews.models import Title, User, Comment, TitleGenre


CSV_FILES = [
    "genre.csv",
    "category.csv",
    "comments.csv",
    "titles.csv",
    "genre_title.csv",
    "review.csv",
    "users.csv",
]

SAVED_MESSAGE = "Данные сохранены"
NOT_SAVED_MESSAGE = "Данные по внешнему ключу не найдены"


class Command(BaseCommand):
    help = "Загрузка данных из CSV файлов"

    def handle(self, *args, **options):
        for csv_file in CSV_FILES:
            with open(f"./static/data/{csv_file}", encoding="utf-8") as file:
                reader = DictReader(file)
                print(f"Идет загрузка данных из {csv_file}...")
                for row in reader:
                    if csv_file == "user.csv":
                        user_load(row)
                    elif csv_file == "category.csv":
                        category_load(row)
                    elif csv_file == "genre.csv":
                        genre_load(row)
                    elif csv_file == "review.csv":
                        review_load(row)
                    elif csv_file == "title.csv":
                        title_load(row)
                    elif csv_file == "comment.csv":
                        comment_load(row)
                    elif csv_file == "genre_title.csv":
                        genre_title_load(row)


def user_load(row):
    user = User(
        id=row["id"],
        username=row["username"],
        email=row["email"],
        role=row["role"],
        bio=row["bio"],
        first_name=row["first_name"],
        last_name=row["last_name"],
    )
    user.save()
    print(SAVED_MESSAGE)


def category_load(row):
    category = Category(id=row["id"], name=row["name"], slug=row["slug"])
    category.save()
    print(SAVED_MESSAGE)


def genre_load(row):
    genre = Genre(id=row["id"], name=row["name"], slug=row["slug"])
    genre.save()
    print(SAVED_MESSAGE)


def review_load(row):
    try:
        title = Title.objects.get(id=row["title_id"])
        review = Review(
            id=row["id"],
            title=title,
            text=row["text"],
            author=row["author"],
            score=row["score"],
            pub_date=row["pub_date"],
        )
        review.save()
        print(SAVED_MESSAGE)
    except ObjectDoesNotExist:
        print(NOT_SAVED_MESSAGE)


def title_load(row):
    try:
        category = Category.objects.get(pk=row["category_id"])
    except ObjectDoesNotExist:
        category = None
    title = Title(
        id=row["id"], name=row["name"], year=row["year"], category=category
    )
    title.save()
    print(SAVED_MESSAGE)


def comment_load(row):
    try:
        review = Review.objects.get(id=row["review_id"])
        comment = Comment(
            id=row["id"],
            review=review,
            text=row["text"],
            author=row["author"],
            pub_date=row["pub_date"],
        )
        comment.save()
        print(SAVED_MESSAGE)
    except ObjectDoesNotExist:
        print(SAVED_MESSAGE)


def genre_title_load(row):
    try:
        genre = Genre.objects.get(pk=row["genre_id"])
        title = Title.objects.get(pk=row["title_id"])
        titlegenre = TitleGenre(id=row["id"], title=title, genre=genre)
        titlegenre.save()
        print(SAVED_MESSAGE)
    except ObjectDoesNotExist:
        print(SAVED_MESSAGE)
