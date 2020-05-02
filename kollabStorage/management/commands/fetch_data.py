from django.core.management.base import BaseCommand, CommandError

from kollabStorage.models import *
from kollabStorage.services import KollabApi


class Command(BaseCommand):
    help = 'Fetch new data from Kollab server'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.kollab_api = KollabApi()

    def fetch_users(self):
        self.stdout.write(self.style.HTTP_INFO('Fetching users...'))
        response = self.kollab_api.get_users()
        self.stdout.write('New or updated users:')
        User.objects.all().delete()

        for user in response:
            new_user, created = User.objects.update_or_create(id=user['id'], defaults=user)
            self.stdout.write(f'\t{new_user.__str__()}')

        self.stdout.write(f'Total users: {len(response)}')
        self.stdout.write(self.style.SUCCESS('Successfully updated users'))

    def fetch_projects(self):
        self.stdout.write(self.style.HTTP_INFO('Fetching projects...'))
        response = self.kollab_api.get_projects()
        self.stdout.write('New or updated projects:')
        Project.objects.all().delete()

        for project in response:
            new_project, created = Project.objects.update_or_create(id=project['id'], defaults=project)
            self.stdout.write(f'\t{new_project.__str__()}')

        self.stdout.write(f'Total projects: {len(response)}')
        self.stdout.write(self.style.SUCCESS('Successfully updated projects'))

    def handle(self, *args, **options):
        self.fetch_users()
        self.fetch_projects()
