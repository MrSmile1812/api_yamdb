from csv import DictReader

from django.core.management import BaseCommand

from reviews.models import Title


class Command(BaseCommand):
    help = "Loads data from genre_title.csv"

    def handle(self, *args, **options):
        print("Loading genre_title data")

        for row in DictReader(open("./static/data/genre_title.csv")):
            genre_title = Title(
                title=row["title_id"],
                genre=row["genre_id"],
            )
            genre_title.save()
