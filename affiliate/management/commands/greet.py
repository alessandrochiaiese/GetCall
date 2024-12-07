from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Saluta l\'utente'

    def add_arguments(self, parser):
        parser.add_argument('name', type=str, help='Il nome dell\'utente da salutare')

    def handle(self, *args, **options):
        name = options['name']
        self.stdout.write(f'Ciao, {name}!')
