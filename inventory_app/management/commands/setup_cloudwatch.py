from django.core.management.base import BaseCommand
from inventory_app.cloudwatch_setup import setup_cloudwatch_dashboard, create_inventory_alarms

class Command(BaseCommand):
    help = 'Setup CloudWatch dashboard and alarms for inventory monitoring'

    def handle(self, *args, **options):
        self.stdout.write('Setting up CloudWatch dashboard...')
        if setup_cloudwatch_dashboard():
            self.stdout.write(self.style.SUCCESS('Dashboard created successfully'))
        else:
            self.stdout.write(self.style.ERROR('Failed to create dashboard'))
        
        self.stdout.write('Creating CloudWatch alarms...')
        create_inventory_alarms()
        self.stdout.write(self.style.SUCCESS('Alarms created successfully'))