from csv import DictReader

from django.core.management import BaseCommand

from reviews.models import Category


ALREDY_LOADED_ERROR_MESSAGE = """
If you need to reload the category data from the CSV file,
first delete the db.sqlite3 file to destroy the database.
Then, run `python manage.py migrate` for a new empty
database with tables"""


class Command(BaseCommand):
    help = "Loads data from category.csv"

    def handle(self, *args, **options):
        if Category.objects.exists():
            print("Category data already loaded...exiting.")
            print(ALREDY_LOADED_ERROR_MESSAGE)
            return

        print("Loading category data")

        for row in DictReader(open("./static/data/category.csv")):
            category = Category(
                name=row["name"],
                slug=row["slug"],
            )
            category.save()
