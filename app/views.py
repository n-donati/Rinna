import base64
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
import xml.etree.ElementTree as ET
import os
from .interest.contract import create_rtf_file
from decimal import Decimal
from django.utils import timezone
from .models import Cedente, Factor, Pool, Facturas, Puja
from django.db.models import Sum
from datetime import datetime, timedelta
from django.db import transaction  # Add this import
from io import BytesIO
import random

def home(request):
    return render(request, 'home.html')

def market(request):
    # Check if database is empty and seed if necessary
    if not Facturas.objects.exists():
        seed_database()
    
    tasaInicial = Facturas.objects.first().interes_firmado    
    if not Pool.objects.exists():
        tasaActual = tasaInicial
    
    try:
        tasaActual = Pool.objects.first().puja_actual
    except:
        tasaActual = Facturas.objects.first().interes_firmado
    cantidadFacturas = Facturas.objects.count()
    volumenFacturas = Facturas.objects.aggregate(total_monto=Sum('monto'))['total_monto']

    return render(request, 'market.html', {'tasaInicial':round(tasaInicial, 2),
                                           'tasaActual':round(tasaActual, 2), 
                                           'cantidadFacturas':cantidadFacturas,
                                           'volumenFacturas':round(volumenFacturas, 2)})

def dashboard(request):
    return render(request, 'dashboard.html')

def login_c(request):
    return render(request, 'login_c.html')

def login_f(request):
    return render(request, 'login_f.html')

def seed_database():
    """Helper function to seed the database with initial data"""
    with transaction.atomic():
        # Create Factor if none exists
        factor, _ = Factor.objects.get_or_create(
            factor='Bancomer',
            rfc='DEF987654321'
        )

        # Create Cedente if none exists
        cedente, _ = Cedente.objects.get_or_create(
            cedente='Sample Provider',
            rfc='ABC123456789'
        )

        # Create some sample Facturas
        for i in range(20):  # Create 5 sample facturas
            factura = Facturas.objects.create(
                ID_cedente=cedente,
                deudor="Costco",
                domicilio_deudor="Sample Address",
                monto=Decimal(random.uniform(5000, 10000)),
                plazo=30,
                interes_firmado=Decimal('2.5')
            )

def pool(request):
    deudor = "Costco"
    
    if request.method == "POST":
        # find factor
        bid_value = request.POST.get('bid')
        pool_id = 1
        
        if float(bid_value) < float(Pool.objects.get(id=pool_id).puja_actual):
            try:
                pool = Pool.objects.get(id=pool_id)
                
                # Create new bid
                Puja.objects.create(
                    ID_pool=pool,
                    ID_factor=Factor.objects.first(),
                    estado_puja=True
                )

                # Update pool's current bid
                pool.puja_actual = pool.puja_actual -  Decimal(bid_value)
                current_time = timezone.now()
                formatted_time = current_time.strftime('%Y-%m-%d %H:%M:%S.%f')
                pool.fecha_puja_actual = formatted_time
                pool.save()
                factor = "Bancomer"
            except (Factor.DoesNotExist, Pool.DoesNotExist):
                pass
    
    # Extracting all facturas from the deudor
    facturas = Facturas.objects.filter(deudor=deudor)

    # Using aggregate to sum up the 'monto' field of filtered facturas
    poolSize = facturas.aggregate(total_monto=Sum('monto'))['total_monto']

    print("poolsize", poolSize) 
    
    # fibonacci calculation
    assigned_pools = assign_pools(poolSize, facturas)
    
    # calculo de subdivision de la pool
    subdivision1 = round(assigned_pools['pool1']['current_total'], 2)
    subdivision2 = round(assigned_pools['pool2']['current_total'], 2)
    subdivision3 = round(assigned_pools['pool3']['current_total'], 2)
    subdivision4 = round(assigned_pools['pool4']['current_total'], 2)
    
    # Get puja_actual safely
    try:
        puja_actual = Facturas.objects.first().interes_firmado
    except (Facturas.DoesNotExist, AttributeError):
        puja_actual = Decimal('0.0000000000')

    # Create a pool for each subdivision in assigned_pools
    if not Pool.objects.filter(deudor=deudor).exists():
        pool_instances = {}
        for pool_name in ['pool1', 'pool2', 'pool3', 'pool4']:
            try:
                pool_instance, created = Pool.objects.get_or_create(
                    deudor=deudor,
                    tamaño=assigned_pools[pool_name]['current_total'],
                    fecha_registro=datetime.now(),
                    puja_actual=puja_actual,
                    fecha_puja_actual=datetime.now()
                )
                pool_instance.save()
                pool_instances[pool_name] = pool_instance
            except Exception as e:
                print(f"Error creating pool {pool_name}: {str(e)}")
                continue
        for pool_name, pool in assigned_pools.items():
            if pool_name in pool_instances:
                for factura_id in pool['facturas']:
                    try:
                        factura = Facturas.objects.get(id=factura_id)
                        factura.ID_pool = pool_instances[pool_name]
                        factura.save()
                    except Facturas.DoesNotExist:
                        continue
    
    # porcentage de PUJA 
    percentage1 = round(Pool.objects.get(id=1).puja_actual, 4)
    percentage2 = round(Pool.objects.get(id=2).puja_actual, 4)
    percentage3 = round(Pool.objects.get(id=3).puja_actual, 4) 
    percentage4 = round(Pool.objects.get(id=4).puja_actual, 4)
    
    bids = []
    factores = ['BBVA', 'BBVA', 'Santander', 'HSBC']
    for id in range(1, 5):
        pool_instance = Pool.objects.get(deudor=deudor, id=id)
        bids.append({
            'id': id,
            'percentage': round(pool_instance.puja_actual, 4),
            'last_puja_time': pool_instance.fecha_puja_actual.strftime('%Y-%m-%d %H:%M:%S.%f'),
            'factor': factores[id - 1]
        })

    return render(request, 'pool.html', {
        'poolSize': round(poolSize, 2),
        'subdivision1': subdivision1,
        'subdivision2': subdivision2,
        'subdivision3': subdivision3,
        'subdivision4': subdivision4,
        'percentage1': percentage1,
        'percentage2': percentage2,
        'percentage3': percentage3,
        'percentage4': percentage4,
        'volumenFacturas': len(facturas),
        'fechaVencimientoSubasta': datetime.now()
    .replace(hour=23, minute=59, second=59),
    'plazoMedioDePago': facturas.aggregate(promedio_plazo=Sum('plazo') / len(facturas))['promedio_plazo'],
    'ofertasTotales': Puja.objects.count(),
    'bids': bids
    })

def assign_pools(poolSize, facturas):
    # Initialize pools with their target sizes and current totals
    pools = {
        'pool1': {'target': poolSize / 2, 'facturas': [], 'current_total': 0},
        'pool2': {'target': poolSize / 4, 'facturas': [], 'current_total': 0},
        'pool3': {'target': poolSize / 8, 'facturas': [], 'current_total': 0},
        'pool4': {'target': poolSize / 8, 'facturas': [], 'current_total': 0}
    }

    # Sort facturas from largest to smallest to improve packing
    facturas_sorted = sorted(facturas, key=lambda x: x.monto, reverse=True)

    # Assign facturas to pools
    for factura in facturas_sorted:
        assigned = False
        for pool_name, pool in pools.items():
            if pool['current_total'] + factura.monto <= pool['target']:
                pool['facturas'].append(factura.id)
                pool['current_total'] += factura.monto
                assigned = True
                break
        
        # Fallback: Assign to the pool with the most remaining capacity
        if not assigned:
            fallback_pool = min(pools.items(), key=lambda x: x[1]['target'] - x[1]['current_total'])[0]
            pools[fallback_pool]['facturas'].append(factura.id)
            pools[fallback_pool]['current_total'] += factura.monto

    # Output the result
    for pool_name, pool in pools.items():
        print(f"Pool: {pool_name}")
        print(f"  Target: {pool['target']}")
        print(f"  Current Total: {pool['current_total']}")
        print(f"  Number of Facturas: {pool['facturas']}")
    
    return pools
def is_valid_xml(file):
    try:
        tree = ET.parse(file)
        root = tree.getroot()
        return True
    except ET.ParseError:
        return False
    except Exception:
        return False

def parse_invoice(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    namespaces = {'cfdi': 'http://www.sat.gob.mx/cfd/4'}
    
    invoice_data = {}
    emisor = root.find('cfdi:Emisor', namespaces)
    receptor = root.find('cfdi:Receptor', namespaces)
    
    if emisor is not None:
        invoice_data['cedente'] = emisor.get('Nombre')
        invoice_data['rfcCedente'] = emisor.get('Rfc')

    if receptor is not None:
        invoice_data['deudor'] = receptor.get('Nombre')
        invoice_data['rfcDeudor'] = receptor.get('Rfc')
        invoice_data['domicilioFiscalReceptor'] = receptor.get('DomicilioFiscalReceptor')
    
    invoice_data['numeroFactura'] = root.get('Folio')
    invoice_data['fechaEmision'] = root.get('Fecha')
    invoice_data['plazo'] = root.get('CondicionesDePago')
    invoice_data['total'] = root.get('Total')
    
    return invoice_data

def calculate_interest(invoice_data):
    interest_rate = 0.02
    delta_days = float(invoice_data['plazo'])
    interest_amount = (float(invoice_data['total']) * delta_days / 365) * (interest_rate / 100)
    return interest_amount + 4

