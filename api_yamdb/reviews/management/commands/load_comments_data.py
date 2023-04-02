from csv import DictReader

from django.core.management import BaseCommand

from reviews.models import Comment


class Command(BaseCommand):
    help = "Loads data from comments.csv"

    def handle(self, *args, **options):
        print("Loading comments data")

        for row in DictReader(open("./static/data/comments.csv")):
            comments = Comment(
                review=row["review_id"],
                text=row["text"],
                author=row["author"],
                pub_date=row["pub_date"],
            )
            comments.save()
