from django.db import models

class Cedente(models.Model):
    cedente = models.CharField(max_length=255)
    rfc = models.CharField(max_length=13)
    fecha_registro = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.cedente

class Factor(models.Model):
    factor = models.CharField(max_length=255)
    rfc = models.CharField(max_length=13)
    domicilio = models.CharField(max_length=255)
    fecha_registro = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.factor

class Pool(models.Model):
    deudor = models.CharField(max_length=255)
    tamaño = models.DecimalField(max_digits=15, decimal_places=2)
    fecha_registro = models.DateField(auto_now_add=True)
    # puja mas alta hasta el momento
    puja_actual = models.DecimalField(max_digits=12, decimal_places=10)
    # factor a la que pertenece puja actual
    ID_factor = models.ForeignKey(Factor, on_delete=models.CASCADE)
    fecha_puja_actual = models.DateField(auto_now_add=True)

class Facturas(models.Model):
    # cedente al que pertenece
    ID_cedente = models.ForeignKey(Cedente, on_delete=models.CASCADE)
    # pool al que pertenece la factura
    ID_pool = models.ForeignKey(Pool, on_delete=models.CASCADE)
    
    xml = models.FileField(upload_to='xml/')
    monto = models.DecimalField(max_digits=15, decimal_places=5)
    # plazo de pago, para hacer display en el pool
    plazo = models.IntegerField()
    interes_firmado = models.DecimalField(max_digits=12, decimal_places=10)
    contrato = models.BinaryField()

class Puja(models.Model):
    ID_pool = models.ForeignKey(Pool, on_delete=models.CASCADE)
    ID_factor = models.ForeignKey(Factor, on_delete=models.CASCADE)
    # si la puja ya fue superada o no
    estado_puja = models.BooleanField()
    # fecha en que la puja fue hecha
    fecha = models.DateField(auto_now_add=True)
