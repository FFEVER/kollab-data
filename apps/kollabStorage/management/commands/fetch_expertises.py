from django.core.management.base import BaseCommand

from apps.kollabStorage.models import Expertise
from apps.kollabStorage import KollabApi


class Command(BaseCommand):
    help = 'Fetch all expertises from Kollab server'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.kollab_api = KollabApi()

    def fetch_expertises(self):
        self.stdout.write(self.style.HTTP_INFO('Fetching expertises...'))
        response = self.kollab_api.get_expertises()
        self.stdout.write('Updated services')

        for expertise in response:
            new_expertise, created = Expertise.objects.update_or_create(id=expertise['id'], defaults=expertise)
            self.stdout.write(f'\t{new_expertise.__str__()}')

        self.stdout.write(f'Total users: {len(response.json())}')

    def handle(self, *args, **options):
        self.fetch_expertises()
        self.stdout.write(self.style.SUCCESS('Successfully updated expertises'))
