# # para leer archivos .rtf
# from pyth.plugins.rtf15.reader import Rtf15Reader
# from pyth.document import Document

# try:
#     # Leer un archivo RTF
#     with open('contract.rtf', 'rb') as file:
#         doc = Rtf15Reader.read(file)

#     # Imprimir el contenido del documento
#     for para in doc.content:
#         print(''.join(element.content for element in para.content))
# except Exception as e:
#     print(f"Error reading RTF file: {e}")

from striprtf.striprtf import rtf_to_text
import aspose.words as aw

# def read_and_print_rtf(filepath):
#     try:
#         with open(filepath, 'r') as file:
#             rtf_content = file.read()
#         text = rtf_to_text(rtf_content)
#         print(text)
#     except FileNotFoundError:
#         print("The file was not found.")
#     except Exception as e:
#         print(f"An error occurred: {e}")

# read_and_print_rtf('contrato.rtf')

def create_rtf_file(cedente, fecha, total, domicilio, ciudad):
    # Crear un nuevo documento.
    doc = aw.Document()
    builder = aw.DocumentBuilder(doc)

    # Configurar los estilos del documento, similar a los encontrados en el RTF original
    font = builder.font
    font.name = "Arial"
    font.size = 12
    builder.paragraph_format.alignment = aw.ParagraphAlignment.JUSTIFY
    
    # Restablecer para el texto normal del documento
    font.bold = True
    font.size = 12
    builder.writeln("CONTRATO DE CESION DE DERECHOS DE COBRO")
    
    # Set the text to be bold.
    builder.font.bold = False 
    # Write a line of bold text.
    builder.writeln(f"CONTRATO DE CESIÓN DE DERECHO DE COBRO ADELANTADO QUE CELEBRAN POR UNA PARTE {cedente}; A QUIEN EN LO SUCESIVO SE LE DENOMINARÁ COMO \"LA PARTE CEDENTE\"; Y POR LA OTRA _______; A QUIEN EN LO SUCESIVO SE LE DENOMINARÁ COMO \"LA PARTE CESIONARIA\"; AMBOS CONTRATANTES DENOMINADOS DE MANERA CONJUNTA COMO \"LAS PARTES\", QUIENES SE OBLIGAN AL TENOR DE LOS SIGUIENTES ANTECEDENTES, DECLARACIONES Y CLÁUSULAS:")
    
    builder.font.bold = True
    builder.writeln("DECLARA \"LA PARTE CEDENTE\"")
    
    expediente = "000001"
    # Set the text to be bold.
    builder.font.bold = False 
    # Write a line of bold text.
    builder.writeln(f"I.- Que {cedente} el día {fecha} contrajo una deuda por la cantidad de ${total} pesos mexicanos (MXN), la cual está respaldada por un documento denominado pagaré; y el cual forma parte del presente contrato estando adjunto al mismo; y que \"LA PARTE CEDENTE\" está tratando de recobrar dicha deuda mediante un juicio al que le fue asignado el número de expediente {expediente}.")
    
    builder.writeln(f"II.- Con fecha {fecha} realizó un pago por la cantidad de ${total} pesos mexicanos (MXN).")
    
    builder.writeln(f"III.- La deuda que está siendo cedida en el presente contrato está garantizado con lo siguiente: Factura electrónica (CFDI 4.0)")
    
    builder.writeln(f"""IV.- Para asegurar el cumplimiento de la obligación materia de transmisión del presente contrato, el acreditado aseguró su pago con lo siguiente:

    V.- Que no existe ninguna acción, judicial o extrajudicial, o algún efecto que perjudique la titularidad o transferencia del derechos de cobro materia del presente contrato.

    VI.- Tener su domicilio en {domicilio}, en la siguiente ciudad: {ciudad}, el cual en este acto señala para oír y recibir todo tipo de notificaciones y documentos.

    VII.- Que es su deseo ceder el derechos de cobro descrito en el presente contrato y que la \"PARTE CEDENTE\" tiene el derecho de cobrar y que es el objeto del mismo contrato.""")
    
    builder.font.bold = True
    builder.writeln("DECLARA \"LA PARTE CESIONARIA\"")
    
    # Set the text to be bold.
    builder.font.bold = False 
    builder.writeln(
    """I.- Que \"LA PARTE CESIONARIA\" está plenamente facultada para la celebración del presente contrato y para asumir y dar cumplimiento a las obligaciones que en el mismo se establecen.

    II.- Que para efectos del presente contrato:

    _______ no presentó documento de identificación al momento de firmar el presente contrato.
    III.- Que cuenta con pleno conocimiento de que \"LA PARTE CEDENTE\" es poseedora del derechos de cobro materia del presente contrato.

    IV.- Que no existe ninguna acción, judicial o extrajudicial, o algún efecto que le perjudique o impida firmar el presente contrato de cesión de derechos de cobro.

    V.- Que los recursos con los que pagará el precio de la cesión de derechos de cobro materia del presente contrato tienen procedencia lícita.

    VI.- Que cuenta con los recursos suficientes para hacer frente a las obligaciones que mediante el presente contrato contrae.

    VII.- Que \"LA PARTE CESIONARIA\" cuenta con todas las facultades para la celebración del presente contrato y no le han sido revocadas, modificadas o limitadas en forma alguna que afecte la validez del presente contrato.

    VIII.- Tener su domicilio en _______, en la siguiente ciudad: _______, _______, el cual en este acto señala para oír y recibir todo tipo de notificaciones y documentos.

    VIII.- Que es su deseo adquirir el derechos de cobro descrito en el presente contrato y que la \"PARTE CEDENTE" tiene el derecho de cobrar y que es el objeto del mismo contrato.

    IX.- Que es su deseo adquirir el derechos de cobro mencionado en las declaraciones de \"LA PARTE CEDENTE\".""")
    
    builder.font.bold = False 
    builder.writeln(f"""Leído que fue el presente contrato por las partes, una vez enteradas de su alcance y fuerza legal, no existiendo vicio de la voluntad que pudiera invalidarlo lo firman "LAS PARTES", por duplicado al margen y al calce, en la Ciudad de {ciudad}, el factor, recibiendo cada una de las partes en este acto copia del mismo.""")
    
    builder.font.bold = True
    builder.writeln(f"""LA PARTE CEDENTE
                    
                    
                    _______________________
                    {cedente}""")
    
    builder.font.bold = False
    builder.writeln("en representación de:")
    
    builder.font.bold = True
    builder.writeln("""LA PARTE CESIONARIA
                    
                    
                    ______________________""")

    # Guardar el documento en formato RTF
    doc.save("miContrato.rtf", aw.SaveFormat.RTF)

fecha = "12 de enero de 2021"
cedente = "Juan Pérez"
total = "1000"
domicilio = "Calle 123"
ciudad = "Ciudad de México"

create_rtf_file(cedente, fecha, total, domicilio, ciudad)