from rest_framework.serializers import ModelSerializer
from .models import Factura, Cliente, Producto


class ClienteSerializer(ModelSerializer):
    class Meta:
        model = Cliente
        fields = ("nombre", "direccion", "contacto")


class ProductoSerializer(ModelSerializer):
    class Meta:
        model = Producto
        fields = ("nombre", "cantidad", "precio_unitario", "precio_total")


class FacturaSerializer(ModelSerializer):
    cliente = ClienteSerializer(many=False)
    productos = ProductoSerializer(many=True)

    class Meta:
        model = Factura
        fields = (
            "id_factura",
            "cliente",
            "fecha_facturacion",
            "productos",
            "total_compra",
        )

    def create(self, validated_data):
        cliente_data = validated_data.pop("cliente")
        productos_data = validated_data.pop("productos")

        # Create Cliente object
        cliente, created = Cliente.objects.get_or_create(**cliente_data)

        # Create Factura object
        factura = Factura.objects.create(cliente=cliente, **validated_data)

        # Create Producto objects
        for producto_data in productos_data:
            Producto.objects.create(factura=factura, **producto_data)

        return factura
