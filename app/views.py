from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
import xml.etree.ElementTree as ET
import os

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

def upload_xml(request):
    if request.method == 'POST':
        if 'xmlFile' not in request.FILES:
            messages.error(request, 'No se seleccionó ningún archivo')
            return redirect('dashboard')
            
        xml_file = request.FILES['xmlFile']
        
        # Validate file size (e.g., max 5MB)
        if xml_file.size > 5 * 1024 * 1024:
            messages.error(request, 'El archivo es demasiado grande. Tamaño máximo: 5MB')
            return redirect('dashboard')
        
        # Check file extension
        if not xml_file.name.endswith('.xml'):
            messages.error(request, 'El archivo debe ser un XML válido')
            return redirect('dashboard')
            
        # Create uploads directory if it doesn't exist
        upload_dir = 'uploads/xml_files'
        os.makedirs(upload_dir, exist_ok=True)
        
        try:
            # Save file temporarily to validate
            fs = FileSystemStorage(location=upload_dir)
            filename = fs.save(xml_file.name, xml_file)
            file_path = os.path.join(upload_dir, filename)
            
            # Validate XML
            with open(file_path, 'rb') as f:
                if not is_valid_xml(f):
                    os.remove(file_path)
                    messages.error(request, 'El archivo XML no es válido')
                    return redirect('dashboard')
            
            # Process the XML file here
            # Add your XML processing logic
            messages.success(request, 'Factura subida exitosamente')
            
        except Exception as e:
            if os.path.exists(file_path):
                os.remove(file_path)
            messages.error(request, f'Error al procesar el archivo: {str(e)}')
            
        return redirect('dashboard')
        
    messages.error(request, 'Método no permitido')
    return redirect('dashboard')
