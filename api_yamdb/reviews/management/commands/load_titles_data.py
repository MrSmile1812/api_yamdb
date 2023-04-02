from csv import DictReader

from django.core.management import BaseCommand

from reviews.models import Title


class Command(BaseCommand):
    help = "Loads data from titles.csv"

    def handle(self, *args, **options):
        print("Loading title data")

        for row in DictReader(open("./static/data/titles.csv")):
            title = Title(
                username=row["username"],
                email=row["email"],
                role=row["role"],
                bio=row["bio"],
                first_name=row["first_name"],
                last_name=row["last_name"],
            )
            title.save()
