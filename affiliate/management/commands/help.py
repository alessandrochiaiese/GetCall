from django.core.management.base import BaseCommand, CommandError
from django.core.management import get_commands, load_command_class

class Command(BaseCommand):
    help = 'Mostra l\'aiuto per tutti i comandi personalizzati'

    def handle(self, *args, **options):
        commands = get_commands()
        for name, app in commands.items():
            if app == 'manager':
                try:
                    command = load_command_class(app, name)
                    self.stdout.write(f'\nCommand: {name}')
                    self.stdout.write(f'{command.help}\n')
                    parser = command.create_parser('manage.py', name)
                    parser.print_help()
                except CommandError:
                    self.stdout.write(f'Errore caricando il comando: {name}')
