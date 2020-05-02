from django.core.management.base import BaseCommand, CommandError

from kollabStorage.models import *
import kollabStorage.services as services


class Command(BaseCommand):
    help = 'Fetch new data from Kollab server'

    def fetch_users(self):
        self.stdout.write(self.style.HTTP_INFO('Fetching data...'))
        response = services.get_users()
        self.stdout.write('New or updated users:')

        for user in response:
            new_user, created = User.objects.update_or_create(id=user['id'], defaults=user)
            self.stdout.write(f'\t{new_user.__str__()}')

        self.stdout.write(f'Total users: {len(response.json())}')

    def handle(self, *args, **options):
        self.fetch_users()
        self.stdout.write(self.style.SUCCESS('Successfully updated data'))
