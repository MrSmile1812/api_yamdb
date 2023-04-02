from csv import DictReader

from django.core.management import BaseCommand

from reviews.models import Review


class Command(BaseCommand):
    help = "Loads data from review.csv"

    def handle(self, *args, **options):
        print("Loading review data")

        for row in DictReader(open("./static/data/review.csv")):
            reviews = Review(
                title=row["title_id"],
                text=row["text"],
                author=row["author"],
                score=row["score"],
                pub_date=row["pub_date"],
            )
            reviews.save()
