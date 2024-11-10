import base64
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
import xml.etree.ElementTree as ET
import os
import aspose.words as aw

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

def create_contract(cedente, fecha, total, domicilio, interest_rate):
    doc = aw.Document()
    builder = aw.DocumentBuilder(doc)

    builder.font.name = "Arial"
    builder.font.size = 12
    builder.paragraph_format.alignment = aw.ParagraphAlignment.JUSTIFY

    builder.font.bold = True
    builder.writeln("CONTRATO DE CESION DE DERECHOS DE COBRO\n")
    
    builder.font.bold = False
    builder.writeln(f"CONTRATO DE CESIÓN DE DERECHO DE COBRO ADELANTADO QUE CELEBRAN POR UNA PARTE {cedente}; A QUIEN EN LO SUCESIVO SE LE DENOMINARÁ COMO \"LA PARTE CEDENTE\"...")
    
    builder.font.bold = True
    builder.writeln("\nDECLARA \"LA PARTE CEDENTE\"")
    
    builder.font.bold = False
    builder.writeln(f"""I.- Que {cedente} el día {fecha} contrajo una deuda por la cantidad de ${total} pesos mexicanos (MXN)...""")
    
    output_path = "contract.rtf"
    doc.save(output_path, aw.SaveFormat.RTF)
    return output_path

def upload_xml(request):
    if request.method == 'POST' and request.FILES.get('xmlFile'):
        try:
            xml_file = request.FILES['xmlFile']
            
            # Create temp directory if it doesn't exist
            if not os.path.exists('temp'):
                os.makedirs('temp')
            
            # Save XML temporarily
            file_path = os.path.join('temp', xml_file.name)
            with open(file_path, 'wb+') as destination:
                for chunk in xml_file.chunks():
                    destination.write(chunk)
            
            # Process XML and generate contract
            invoice_data = parse_invoice(file_path)
            interest_rate = calculate_interest(invoice_data)
            
            # Generate contract
            contract_path = create_contract(
                invoice_data['cedente'],
                invoice_data['fechaEmision'],
                invoice_data['total'],
                invoice_data['domicilioFiscalReceptor'],
                interest_rate
            )
            
            # Prepare response
            with open(contract_path, 'rb') as f:
                response = HttpResponse(f.read(), content_type='application/rtf')
                response['Content-Disposition'] = 'attachment; filename="contrato.rtf"'
            
            # Cleanup
            os.remove(file_path)
            os.remove(contract_path)
            
            return response
            
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
            return redirect('dashboard')
    
    return redirect('dashboard')

def download_contract(request, filename):
    # This function is no longer needed since we're handling the download in JavaScript
    pass