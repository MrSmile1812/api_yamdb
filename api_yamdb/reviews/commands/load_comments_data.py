from csv import DictReader

from django.core.management import BaseCommand

from reviews.models import Comment


ALREDY_LOADED_ERROR_MESSAGE = """
If you need to reload the comments data from the CSV file,
first delete the db.sqlite3 file to destroy the database.
Then, run `python manage.py migrate` for a new empty
database with tables"""


class Command(BaseCommand):
    help = "Loads data from comments.csv"

    def handle(self, *args, **options):
        if Comment.objects.exists():
            print("Comments data already loaded...exiting.")
            print(ALREDY_LOADED_ERROR_MESSAGE)
            return

        print("Loading comments data")

        for row in DictReader(open("./static/data/comments.csv")):
            comments = Comment(
                review=row["review_id"],
                text=row["text"],
                author=row["author"],
                pub_date=row["pub_date"],
            )
            comments.save()
