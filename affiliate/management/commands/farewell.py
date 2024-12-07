from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Saluta l\'utente con un addio'

    def add_arguments(self, parser):
        parser.add_argument('name', type=str, help='Il nome dell\'utente a cui dire addio')

    def handle(self, *args, **options):
        name = options['name']
        self.stdout.write(f'Addio, {name}!')
