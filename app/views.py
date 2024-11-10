
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
from .models import Cedente, Factor, Pool, Facturas

def home(request):
    return render(request, 'home.html')

def market(request):
    return render(request, 'market.html')

def dashboard(request):
    return render(request, 'dashboard.html')

def login_c(request):
    return render(request, 'login_c.html')

def login_f(request):
    return render(request, 'login_f.html')

def pool(request):
    deudor = "Costco"
    if request.method == "POST":
        # find factor
        bid_value = request.POST.get('bid')
        # get 
        if bid_value:
            print(bid_value)
    
    # Extracting all facturas from the deudor
    facturas = Facturas.objects.filter(deudor=deudor)

    # Using aggregate to sum up the 'monto' field of filtered facturas
    poolSize = facturas.aggregate(total_monto=Sum('monto'))['total_monto']

    if poolSize is None:
        print("No facturas found for the deudor.")
        poolSize = 0  # If there are no facturas, set poolSize to 0 to avoid errors

    print("poolsize", poolSize)
    
    # fibonacci calculation
    assigned_pools = assign_pools(poolSize, facturas)
    
    # poolSize = 100
    # historial de pujas 
    calculatedInterest = "4%"
    firstLastInterest = "5%"
    secondLastInterest = "6%"
    thirdLastInterest = "7%"
    fourthLastInterest = "8%"
    fifthLastInterest = "9%"
    
    # calculo de subdivision de la pool
    subdivision1 = round(assigned_pools['pool1']['current_total'], 2)
    subdivision2 = round(assigned_pools['pool2']['current_total'], 2)
    subdivision3 = round(assigned_pools['pool3']['current_total'], 2)
    subdivision4 = round(assigned_pools['pool4']['current_total'], 2)
    
    print(subdivision1+subdivision2+subdivision3+subdivision4)
    
    # porcentage de PUJA 
    percentage1 = round(subdivision1 / poolSize * 100, 2)
    percentage2 = round(subdivision2 / poolSize * 100, 2)
    percentage3 = round(subdivision3 / poolSize * 100, 2)  
    percentage4 = round(subdivision4 / poolSize * 100, 2)
    
    puja_actual = Facturas.objects.first().interes_firmado

    # Create a pool for each subdivision in assigned_pools
    pool_instances = {}
    for pool_name in ['pool1', 'pool2', 'pool3', 'pool4']:
        pool_instance, created = Pool.objects.get_or_create(
            deudor=deudor,
            tamaño=assigned_pools[pool_name]['current_total'],
            fecha_registro=datetime.now(),
            puja_actual=puja_actual,
            fecha_puja_actual=datetime.now()
        )
        pool_instance.save()
        pool_instances[pool_name] = pool_instance

    # Assign facturas to the correct pool
    for pool_name, pool in assigned_pools.items():
        for factura_id in pool['facturas']:
            factura = Facturas.objects.get(id=factura_id)
            factura.ID_pool = pool_instances[pool_name]
            factura.save()

    return render(request, 'pool.html', {
        'calculatedInterest': calculatedInterest,
        'firstLastInterest': firstLastInterest,
        'secondLastInterest': secondLastInterest,
        'thirdLastInterest': thirdLastInterest,
        'fourthLastInterest': fourthLastInterest,
        'fifthLastInterest': fifthLastInterest,
        'poolSize': round(poolSize, 2),
        'subdivision1': subdivision1,
        'subdivision2': subdivision2,
        'subdivision3': subdivision3,
        'subdivision4': subdivision4,
        'percentage1': percentage1,
        'percentage2': percentage2,
        'percentage3': percentage3,
        'percentage4': percentage4,
        # 'facturas': facturas
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

def upload_xml(request):
    if request.method == 'POST' and request.FILES.get('xmlFile'):
        try:
            xml_file = request.FILES['xmlFile']
            
            # Store the binary content of the XML file
            xml_content = xml_file.read()  # This reads the file as binary
            
            # Create a new file-like object for parsing
            from io import BytesIO
            xml_for_parsing = BytesIO(xml_content)
            
            # Parse XML using the file-like object
            invoice_data = parse_invoice(xml_for_parsing)
            interest_rate = calculate_interest(invoice_data)
            
            # Generate contract
            contract_path = "NUEVOCONTRATO.rtf"
            create_rtf_file(
                invoice_data['cedente'],
                invoice_data['fechaEmision'],
                invoice_data['total'],
                invoice_data['domicilioFiscalReceptor'],
                interest_rate
            )
            
            # Get or create Cedente
            cedente_obj, _ = Cedente.objects.get_or_create(
                cedente=invoice_data['cedente'],
                defaults={'rfc': invoice_data['rfcCedente']}
            )
            
            # Get or create Factor
            factor_obj = Factor.objects.first()
            if not factor_obj:
                factor_obj = Factor.objects.create(
                    factor='Default Factor',
                    rfc='DEFAULT000000'
                )
            
            # Create Pool
            pool_obj = Pool.objects.create(
                deudor=invoice_data['deudor'],
                tamaño=Decimal(invoice_data['total']).quantize(Decimal('0.01')),
                puja_actual=Decimal('0.0000000000'),
                ID_factor=factor_obj
            )
            
            # Create Facturas with the XML blob
            with open(contract_path, 'rb') as contract_file:
                contract_content = contract_file.read()
                
                factura = Facturas(
                    ID_cedente=cedente_obj,
                    ID_pool=pool_obj,
                    domicilio_deudor=invoice_data.get('domicilioFiscalReceptor'),
                    deudor=invoice_data['deudor'],
                    xml=xml_content,  # Use the binary content directly
                    monto=Decimal(invoice_data['total']).quantize(Decimal('0.00001')),
                    plazo=int(invoice_data['plazo']),
                    interes_firmado=Decimal(str(interest_rate)).quantize(Decimal('0.0000000000')),
                    contrato=contract_content
                )
                factura.save()
            
            # Prepare response
            response = HttpResponse(contract_content, content_type='application/rtf')
            response['Content-Disposition'] = 'attachment; filename="contrato.rtf"'
            
            # Cleanup
            os.remove(contract_path)
            
            return response
            
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
            return redirect('dashboard')
    
    return redirect('dashboard')

def download_contract(request, filename):
    # This function is no longer needed since we're handling the download in JavaScript
    pass
