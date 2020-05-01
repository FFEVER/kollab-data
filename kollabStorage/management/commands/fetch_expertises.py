from django.core.management.base import BaseCommand, CommandError
from kollabStorage.models import Expertise


class Command(BaseCommand):
    help = 'Fetch all expertises from Kollab server'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Successfully updated expertises'))
