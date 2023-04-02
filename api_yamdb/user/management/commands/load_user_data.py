from csv import DictReader

from django.core.management import BaseCommand

from user.models import User


class Command(BaseCommand):
    help = "Loads data from users.csv"

    def handle(self, *args, **options):
        print("Loading users data")

        for row in DictReader(open("./static/data/users.csv")):
            user = User(
                username=row["username"],
                email=row["email"],
                role=row["role"],
                bio=row["bio"],
                first_name=row["first_name"],
                last_name=row["last_name"],
            )
            user.save()
