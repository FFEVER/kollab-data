from django.core.management.base import BaseCommand, CommandError
from kollabStorage.models import *


class Command(BaseCommand):
    help = 'Fetch new data from Kollab server'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Successfully updated data'))
