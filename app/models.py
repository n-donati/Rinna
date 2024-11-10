from django.db import models

class Cedente(models.Model):
    cedente = models.CharField(max_length=255)
    rfc = models.CharField(max_length=13)
    fecha_registro = models.DateField(auto_now_add=True)

    def str(self):
        return self.cedente

class Factor(models.Model):
    factor = models.CharField(max_length=255)
    rfc = models.CharField(max_length=13)
    fecha_registro = models.DateField(auto_now_add=True)

    def str(self):
        return self.factor

# class Deudor(models.Model):
#     deudor = models.CharField(max_length=255, default="Costco")
#     tamaño = models.DecimalField(max_digits=15, decimal_places=2, default=0)
#     fecha_registro = models.DateField(auto_now_add=True)

class Pool(models.Model):
    # deudor a la que pertenece el pool
    deudor = models.CharField(max_length=255, null=True, default="Costco")
    tamaño = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    fecha_registro = models.DateField(auto_now_add=True)
    # puja mas alta hasta el momento
    puja_actual = models.DecimalField(max_digits=12, decimal_places=10)
    fecha_puja_actual = models.DateField(default=None)

class Facturas(models.Model):
    # cedente al que pertenece
    ID_cedente = models.ForeignKey(Cedente, on_delete=models.CASCADE)
    domicilio_deudor = models.CharField(max_length=255, null=True)
    deudor = models.CharField(max_length=255, null=True)
    domicilio_deudor = models.CharField(max_length=255, null=True)
    deudor = models.CharField(max_length=255, null=True)
    # pool al que pertenece la factura
    ID_pool = models.ForeignKey(Pool, on_delete=models.CASCADE, null=True)
    ID_pool = models.ForeignKey(Pool, on_delete=models.CASCADE, null=True)
    
    xml = models.BinaryField(null=True)
    xml = models.BinaryField(null=True)
    monto = models.DecimalField(max_digits=15, decimal_places=5)
    # plazo de pago, para hacer display en el pool
    plazo = models.IntegerField()
    interes_firmado = models.DecimalField(max_digits=12, decimal_places=10)
    contrato = models.BinaryField(null=True)
    contrato = models.BinaryField(null=True)

class Puja(models.Model):
    ID_pool = models.ForeignKey(Pool, on_delete=models.CASCADE)
    ID_factor = models.ForeignKey(Factor, on_delete=models.CASCADE, default=1)
    # si la puja ya fue superada o no
    estado_puja = models.BooleanField()
    # fecha en que la puja fue hecha
    fecha = models.DateField(auto_now_add=True)