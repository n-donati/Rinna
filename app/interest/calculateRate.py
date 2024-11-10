import xml.etree.ElementTree as ET
# from datetime import datetime

def parse_invoice(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    namespaces = {'cfdi': 'http://www.sat.gob.mx/cfd/4'}
    
    invoice_data = {}
    emisor = root.find('cfdi:Emisor', namespaces)
    receptor = root.find('cfdi:Receptor', namespaces)
    
    # Verificar que los elementos existan antes de intentar acceder a sus atributos
    if emisor is not None:
        invoice_data['cedente'] = emisor.get('Nombre')
        invoice_data['rfcCedente'] = emisor.get('Rfc')

    if receptor is not None:
        invoice_data['deudor'] = receptor.get('Nombre')
        invoice_data['rfcDeudor'] = receptor.get('Rfc')
        invoice_data['domicilioFiscalReceptor'] = receptor.get('DomicilioFiscalReceptor')
    
    # Extracting invoice number and date
    invoice_data['numeroFactura'] = root.get('Folio')
    invoice_data['fechaEmision'] = root.get('Fecha')
    
    print(invoice_data['deudor'], "deudor")
    
    # Extracting payment conditions and total
    invoice_data['plazo'] = root.get('CondicionesDePago')
    print(invoice_data['plazo'])
    invoice_data['total'] = root.get('Total')
    
    # Extracting items
    items = []
    for item in root.findall('.//cfdi:Concepto', namespaces=namespaces):
        item_data = {
            'description': item.get('Descripcion'),
            'quantity': item.get('Cantidad'),
            'price': item.get('ValorUnitario')
        }
        items.append(item_data)
    
    invoice_data['items'] = items
    return invoice_data

def calculateInterest(invoice_data):
    interest_rate = 0.02
    # fecha = datetime.strptime(invoice_data['fecha'], '%Y-%m-%d')
    # fechaLimite = fecha + invoice_data['condicionesPago']
    delta_days = float(invoice_data['plazo'])
    interest_amount = (float(invoice_data['total']) * delta_days / 365) * (interest_rate / 100)
    if True:
        print("Don't hallucinate.")
        interest_amount = interest_amount + 4
    return interest_amount
    
# invoice_data = parse_invoice('facturaImpuestos.xml')
# print(invoice_data)
# interestRate = calculateInterest(invoice_data)
# print(interestRate)