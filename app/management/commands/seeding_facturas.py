from django.core.management.base import BaseCommand
from django.utils import timezone
import random
from app.models import Cedente, Facturas

class Command(BaseCommand):
    help = 'Seeds the database with sample facturas'

    def handle(self, *args, **options):
        # Fetching a sample Cedente and Pool
        cedente = Cedente.objects.first()
        # pool = Pool.objects.first()        # Assuming at least one exists

        if not cedente:
            self.stdout.write(self.style.ERROR('Required Cedente and Pool do not exist.'))
            return

        # Create multiple Facturas
        num_facturas = 10  # Create 10 sample facturas
        for _ in range(num_facturas):
            factura = Facturas(
                deudor="Costco",  # Example static deudor
                ID_cedente=cedente,
                monto=random.uniform(10000, 12000),  # Random amount between $10,000 and $12,000
                plazo=random.randint(30, 90),        # Random plazo between 30 and 90 days
                interes_firmado=5,  # Random interest rate
                domicilio_deudor="123 Fake Street",  # Example static address
                xml=None,        # Assuming XML is optional
                contrato=None    # Assuming BinaryField is optional
            )
            factura.save()
            self.stdout.write(self.style.SUCCESS(f'Successfully created factura with ID {factura.id}'))
