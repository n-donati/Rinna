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

def pool(request, store_name):
    return render(request, 'pool.html', {'store_name': store_name})

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


