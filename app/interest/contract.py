import aspose.words as aw

def create_rtf_file(cedente, fecha, total, domicilio, interestRate):
    doc = aw.Document()
    builder = aw.DocumentBuilder(doc)

    font = builder.font
    font.name = "Arial"
    font.size = 12
    builder.paragraph_format.alignment = aw.ParagraphAlignment.JUSTIFY
    
    font.bold = True
    font.size = 12
    builder.writeln("""CONTRATO DE CESION DE DERECHOS DE COBRO
                    """)
    
    builder.font.bold = False 

    builder.writeln(f"CONTRATO DE CESIÓN DE DERECHO DE COBRO ADELANTADO QUE CELEBRAN POR UNA PARTE {cedente}; A QUIEN EN LO SUCESIVO SE LE DENOMINARÁ COMO \"LA PARTE CEDENTE\"; Y POR LA OTRA _______; A QUIEN EN LO SUCESIVO SE LE DENOMINARÁ COMO \"LA PARTE CESIONARIA\"; AMBOS CONTRATANTES DENOMINADOS DE MANERA CONJUNTA COMO \"LAS PARTES\", QUIENES SE OBLIGAN AL TENOR DE LOS SIGUIENTES ANTECEDENTES, DECLARACIONES Y CLÁUSULAS:")
    
    builder.font.bold = True
    builder.writeln("""
                    DECLARA \"LA PARTE CEDENTE\"""")
    
    expediente = "00001"
    # Set the text to be bold.
    builder.font.bold = False 

    builder.writeln(f"I.- Que {cedente} el día {fecha} contrajo una deuda por la cantidad de ${total} pesos mexicanos (MXN), la cual está respaldada por un documento denominado pagaré; y el cual forma parte del presente contrato estando adjunto al mismo; y que \"LA PARTE CEDENTE\" está tratando de recobrar dicha deuda mediante un juicio al que le fue asignado el número de expediente {expediente}.")
    
    builder.writeln(f"II.- Con fecha {fecha} realizó un pago por la cantidad de ${total} pesos mexicanos (MXN).")
    
    builder.writeln(f"III.- La deuda que está siendo cedida en el presente contrato está garantizado con lo siguiente: Factura electrónica (CFDI 4.0)")
    
    builder.writeln(f"""IV.- Para asegurar el cumplimiento de la obligación materia de transmisión del presente contrato, el acreditado aseguró su pago con lo siguiente:

    V.- Que no existe ninguna acción, judicial o extrajudicial, o algún efecto que perjudique la titularidad o transferencia del derechos de cobro materia del presente contrato.

    VI.- Tener su domicilio en {domicilio}, el cual en este acto señala para oír y recibir todo tipo de notificaciones y documentos.

    VII.- Que es su deseo ceder el derechos de cobro descrito en el presente contrato y que la \"PARTE CEDENTE\" tiene el derecho de cobrar y que es el objeto del mismo contrato con una TASA DE INTERÉS MÁXIMA DE {interestRate} del total de la factura.
    
    VIII.- Que es su deseo ceder el derecho de cobro con una COMISIÓN DE DESCUENTO MÁXIMA DE {interestRate}, siendo RINNA FACTORING SOLUTIONS autorizada para reducir la comisión de descuento a partir de la subasta de la factura.
    
    IX.- Que RINNA FACTORING SOLUTIONS se reserva el derecho de ofrecer el derecho de cobro a un tercero en el momento que el bloque de la factura sea liberado, y entonces pagar el costo de la factura.
    """)
        
    builder.font.bold = True
    builder.writeln("DECLARA \"LA PARTE CESIONARIA\"")
    
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

    VIII.- Tener su domicilio en _______, el cual en este acto señala para oír y recibir todo tipo de notificaciones y documentos.

    VIII.- Que es su deseo adquirir el derechos de cobro descrito en el presente contrato y que la \"PARTE CEDENTE" tiene el derecho de cobrar y que es el objeto del mismo contrato.

    IX.- Que es su deseo adquirir el derechos de cobro mencionado en las declaraciones de \"LA PARTE CEDENTE\".""")
    
    builder.font.bold = False 
    builder.writeln(f"""Leído que fue el presente contrato por las partes, una vez enteradas de su alcance y fuerza legal, no existiendo vicio de la voluntad que pudiera invalidarlo lo firman "LAS PARTES", por duplicado al margen y al calce, a través de RINNA FACTORING SOLUTIONS, el factor, recibiendo cada una de las partes en este acto copia del mismo.
                    
                    
                    
                    
                    
                    
                    
                    """)
    
    builder.font.bold = True
    builder.writeln(f"""LA PARTE CEDENTE
                    

                    _______________________
                    {cedente}""")
    
    builder.font.bold = False
    builder.writeln("""
                    en representación de:
                    """)
    
    builder.font.bold = True
    builder.writeln("""LA PARTE CESIONARIA
                    

                    ______________________""")

    doc.save("NUEVOCONTRATO.rtf", aw.SaveFormat.RTF)