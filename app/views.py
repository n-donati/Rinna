import base64
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
import xml.etree.ElementTree as ET
import os
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
            xml_content = xml_file.read()
            
            # Create a BytesIO object for parsing
            from io import BytesIO
            xml_for_parsing = BytesIO(xml_content)
            
            # Parse XML
            invoice_data = parse_invoice(xml_for_parsing)
            interest_rate = calculate_interest(invoice_data)
            
            # Get or create database objects
            cedente_obj, _ = Cedente.objects.get_or_create(
                cedente=invoice_data['cedente'],
                defaults={'rfc': invoice_data['rfcCedente']}
            )
            
            factor_obj = Factor.objects.first() or Factor.objects.create(
                factor='Default Factor',
                rfc='DEFAULT000000'
            )
            
            pool_obj = Pool.objects.create(
                deudor=invoice_data['deudor'],
                tamaño=Decimal(invoice_data['total']).quantize(Decimal('0.01')),
                puja_actual=Decimal('0.0000000000'),
                ID_factor=factor_obj
            )
            
            # Generate contract text first as string
            contract_text = f"""CONTRATO DE CESION DE DERECHOS DE COBRO

Cedente: {invoice_data['cedente']}
Fecha: {invoice_data['fechaEmision']}
Monto: ${invoice_data['total']}
Domicilio: {invoice_data.get('domicilioFiscalReceptor', 'N/A')}
Tasa de Interés: {interest_rate}%

[Este es un contrato simplificado para demostración]"""
            
            # Create Facturas entry with properly encoded content
            factura = Facturas(
                ID_cedente=cedente_obj,
                ID_pool=pool_obj,
                domicilio_deudor=invoice_data.get('domicilioFiscalReceptor'),
                deudor=invoice_data['deudor'],
                xml=xml_content,
                monto=Decimal(invoice_data['total']).quantize(Decimal('0.00001')),
                plazo=int(invoice_data['plazo']),
                interes_firmado=Decimal(str(interest_rate)).quantize(Decimal('0.0000000000')),
                contrato=contract_text.encode('utf-8')  # Explicitly encode as UTF-8
            )
            factura.save()
            
            # Return the contract as a text file download
            response = HttpResponse(contract_text, content_type='text/plain; charset=utf-8')
            response['Content-Disposition'] = 'attachment; filename="contrato.txt"'
            return response
            
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
            return redirect('dashboard')
    
    return redirect('dashboard')

def download_contract(request, filename):
    # This function is no longer needed since we're handling the download in JavaScript
    pass


