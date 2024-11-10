from django.shortcuts import render, redirect
from django.http import JsonResponse, FileResponse, HttpResponse
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
        # Add any specific XML validation logic here
        # For example, check for required elements
        return True
    except ET.ParseError:
        return False
    except Exception:
        return False

def parse_invoice(file_path):
    tree = ET.parse(file_path)
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

def calculateInterest(invoice_data):
    interest_rate = 0.02
    delta_days = float(invoice_data['plazo'])
    interest_amount = (float(invoice_data['total']) * delta_days / 365) * (interest_rate / 100)
    return interest_amount + 4

def create_rtf_contract(invoice_data, interest_rate):
    doc = aw.Document()
    builder = aw.DocumentBuilder(doc)

    font = builder.font
    font.name = "Arial"
    font.size = 12
    builder.paragraph_format.alignment = aw.ParagraphAlignment.JUSTIFY
    
    # Add contract header
    font.bold = True
    builder.writeln("CONTRATO DE CESION DE DERECHOS DE COBRO")
    
    # Add contract body using invoice data
    builder.font.bold = False
    builder.writeln(f"""CONTRATO DE CESIÓN DE DERECHO DE COBRO ADELANTADO QUE CELEBRAN POR UNA PARTE {invoice_data['cedente']}; 
                    A QUIEN EN LO SUCESIVO SE LE DENOMINARÁ COMO "LA PARTE CEDENTE"...""")
    
    # Add all contract sections using invoice_data
    builder.writeln(f"""I.- Que {invoice_data['cedente']} el día {invoice_data['fechaEmision']} contrajo una deuda 
                    por la cantidad de ${invoice_data['total']} pesos mexicanos (MXN)...""")
    
    # Add more contract sections here using invoice_data and interest_rate
    
    contract_path = os.path.join('uploads', 'contracts', f'contract_{invoice_data["numeroFactura"]}.rtf')
    doc.save(contract_path, aw.SaveFormat.RTF)
    return contract_path

def upload_xml(request):
    if request.method == 'POST':
        try:
            if 'xmlFile' not in request.FILES:
                messages.error(request, 'No se seleccionó ningún archivo')
                return redirect('dashboard')
                
            xml_file = request.FILES['xmlFile']
            
            if xml_file.size > 5 * 1024 * 1024:  # 5MB limit
                messages.error(request, 'El archivo es demasiado grande. Tamaño máximo: 5MB')
                return redirect('dashboard')
            
            if not xml_file.name.endswith('.xml'):
                messages.error(request, 'El archivo debe ser un XML válido')
                return redirect('dashboard')
                
            upload_dir = 'uploads/xml_files'
            contract_dir = 'uploads/contracts'
            os.makedirs(upload_dir, exist_ok=True)
            os.makedirs(contract_dir, exist_ok=True)
            
            fs = FileSystemStorage(location=upload_dir)
            filename = fs.save(xml_file.name, xml_file)
            file_path = os.path.join(upload_dir, filename)
            
            # Process XML and create contract
            invoice_data = parse_invoice(file_path)
            interest_rate = calculateInterest(invoice_data)
            contract_path = create_rtf_contract(invoice_data, interest_rate)
            
            # Create response with contract file
            with open(contract_path, 'rb') as contract_file:
                response = HttpResponse(
                    contract_file.read(),
                    content_type='application/rtf'
                )
                response['Content-Disposition'] = f'attachment; filename=contract_{invoice_data["numeroFactura"]}.rtf'
                
            # Clean up files
            if os.path.exists(file_path):
                os.remove(file_path)
            if os.path.exists(contract_path):
                os.remove(contract_path)
                
            messages.success(request, 'Factura procesada exitosamente')
            return response
            
        except Exception as e:
            messages.error(request, f'Error al procesar el archivo: {str(e)}')
            if 'file_path' in locals() and os.path.exists(file_path):
                os.remove(file_path)
            return redirect('dashboard')
    
    return redirect('dashboard')
