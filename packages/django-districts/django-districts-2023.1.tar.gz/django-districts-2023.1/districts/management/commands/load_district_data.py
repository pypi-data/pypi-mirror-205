from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
    help = 'Loads the initial data for the districts package, python manage.py load_district_data'

    def handle(self, *args, **options):
        call_command('loaddata', 'data.json', app_label='districts')