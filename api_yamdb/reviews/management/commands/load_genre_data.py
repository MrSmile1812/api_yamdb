from csv import DictReader

from django.core.management import BaseCommand

from reviews.models import Genre


class Command(BaseCommand):
    help = "Loads data from genre.csv"

    def handle(self, *args, **options):
        print("Loading genre data")

        for row in DictReader(open("./static/data/genre.csv")):
            genre = Genre(
                name=row["name"],
                slug=row["slug"],
            )
            genre.save()
