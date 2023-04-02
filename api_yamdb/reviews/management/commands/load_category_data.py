from csv import DictReader

from django.core.management import BaseCommand

from reviews.models import Category


class Command(BaseCommand):
    help = "Loads data from category.csv"

    def handle(self, *args, **options):
        print("Loading category data")

        for row in DictReader(open("./static/data/category.csv")):
            category = Category(
                name=row["name"],
                slug=row["slug"],
            )
            category.save()
