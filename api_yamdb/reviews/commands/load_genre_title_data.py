from csv import DictReader

from django.core.management import BaseCommand

from reviews.models import GenreTitle


ALREDY_LOADED_ERROR_MESSAGE = """
If you need to reload the genre_title data from the CSV file,
first delete the db.sqlite3 file to destroy the database.
Then, run `python manage.py migrate` for a new empty
database with tables"""


class Command(BaseCommand):
    help = "Loads data from genre_title.csv"

    def handle(self, *args, **options):
        if GenreTitle.objects.exists():
            print("Genre_title data already loaded...exiting.")
            print(ALREDY_LOADED_ERROR_MESSAGE)
            return

        print("Loading genre_title data")

        for row in DictReader(open("./static/data/genre_title.csv")):
            genre_title = GenreTitle(
                title=row["title_id"],
                genre=row["genre_id"],
            )
            genre_title.save()
