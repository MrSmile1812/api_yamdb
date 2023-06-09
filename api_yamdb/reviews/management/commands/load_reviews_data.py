from csv import DictReader

from django.core.management import BaseCommand

from reviews.models import Category, Comment, Genre, Review, Title
from user.models import User


ALREDY_LOADED_ERROR_MESSAGE = """
If you need to reload the child data from the CSV file,
first delete the db.sqlite3 file to destroy the database.
Then, run `python manage.py migrate` for a new empty
database with tables"""

TABLES = {
    User: "users.csv",
    Category: "category.csv",
    Genre: "genre.csv",
    Title: "titles.csv",
    Review: "review.csv",
    Comment: "comments.csv",
    Title.genre.through: "genre_title.csv",
}


class Command(BaseCommand):
    help = "Loads data from csv files"

    def handle(self, *args, **kwargs):
        for model, csv in TABLES.items():
            with open(f"./static/data/{csv}", encoding="utf-8") as file:
                if model.objects.exists():
                    self.stdout.write(
                        self.style.WARNING(
                            f"{model} data already loaded...exiting."
                        )
                    )
                    self.stdout.write(ALREDY_LOADED_ERROR_MESSAGE)
                    continue
                reader = DictReader(file)
                model.objects.bulk_create(model(**data) for data in reader)
            self.stdout.write(self.style.SUCCESS("Все данные загружены"))
