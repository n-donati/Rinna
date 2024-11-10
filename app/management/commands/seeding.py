from django.core.management.base import BaseCommand
from app.models import Cedente, Pool, Facturas, Factor
import random
from datetime import timezone, datetime

PROVIDERS = [
    'Fresh Farms',
    'Green Valley Organics',
    'Dairy Delight',
    'Baker\'s Best',
    'Seafood Select',
    'Meat Masters',
    'Fruit Fiesta',
    'Veggie Ventures',
    'Grain Goods',
    'Snack Station'
]

class Command(BaseCommand):
    help = 'Seeds the database with basic entities like Cedente, Factor, and Pool.'

    def handle(self, *args, **options):
        self.creating_basics()

    def creating_basics(self):
        # Create or get a Cedente
        cedente, created = Cedente.objects.get_or_create(
            cedente=PROVIDERS[random.randint(0, len(PROVIDERS) - 1)],
            rfc='ABC123456789',
        )

        # Create or get a Factor
        factor, created = Factor.objects.get_or_create(
            factor='Bancomer',
            rfc='DEF987654321',
        )

        # Create or get a Pool that relates to the 'deudor'
        # pool, created = Pool.objects.get_or_create(
        #     deudor='Costco',  # This name should be consistent for your requirement
        #     tamaño=0.00,  # Assuming you have a 'tamaño' field
        #     puja_actual=4.16,
        #     fecha_puja_actual=datetime.now(timezone.utc),
        # )

        # Confirm creations
        if created:
            self.stdout.write(self.style.SUCCESS(f'Cedente created: {cedente}'))
        else:
            self.stdout.write(self.style.WARNING(f'Cedente already exists: {cedente}'))

