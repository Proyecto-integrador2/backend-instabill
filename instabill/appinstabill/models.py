import os
from django.db import models

# Create your models here.


class Cliente(models.Model):
    id_cliente = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=128)
    direccion = models.CharField(max_length=128)
    contacto = models.CharField(max_length=128)

    def __str__(self):
        return f"Cliente: {self.nombre}"


class Factura(models.Model):
    id_factura = models.AutoField(primary_key=True)
    cliente = models.ForeignKey(
        Cliente, on_delete=models.CASCADE, db_column="id_cliente"
    )
    fecha_facturacion = models.CharField(max_length=256)
    total_compra = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"Fecha Factura: {self.date}"


class Producto(models.Model):
    id_producto = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=128)
    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=12, decimal_places=2)
    precio_total = models.DecimalField(max_digits=12, decimal_places=2)
    factura = models.ForeignKey(
        Factura,
        on_delete=models.CASCADE,
        related_name="productos",
        db_column="id_factura",
    )

    def __str__(self):
        return f"Producto: {self.nombre}"
