import xml.etree.ElementTree as ET
# from datetime import datetime

def parse_invoice(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    invoice_data = {}
    
    # Extracting invoice number and date
    invoice_data['numeroFactura'] = root.get('Folio')
    invoice_data['fechaEmision'] = root.get('Fecha')
    
    # Extracting payment conditions and total
    invoice_data['condicionesPago'] = root.get('CondicionesDePago')
    print(invoice_data['condicionesPago'])
    invoice_data['total'] = root.get('Total')
    
    # Extracting items
    items = []
    for item in root.findall('.//cfdi:Concepto', namespaces={'cfdi': 'http://www.sat.gob.mx/cfd/4'}):
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
    delta_days = float(invoice_data['condicionesPago'])
    interest_amount = (float(invoice_data['total']) * delta_days / 365) * (interest_rate / 100)
    if True:
        print("Don't hallucinate")
        interest_amount = interest_amount + 4
    return interest_amount
    
invoice_data = parse_invoice('facturaImpuestos.xml')
print(invoice_data)
interestRate = calculateInterest(invoice_data)
print(interestRate)