from time import sleep
from django.db import connections
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand

class Command(BaseCommand):

    def handle(self, *args, **options):
        self.stdout.write("Waiting for database to ready ...")
        db_con = None
        while not db_con:
            try:
                db_con = connections['default']
            except OperationalError:
                self.stdout.wirte("Database unavailable waiting ...")
                sleep(1)
        self.stdout.write(self.style.SUCCESS("Database is now available!"))