from rest_framework import serializers
from .models import Pedido, LineaPedido

class LineaPedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = LineaPedido
        fields = ['id', 'producto', 'referencia', 'cantidad']

class PedidoSerializer(serializers.ModelSerializer):
    lineas = LineaPedidoSerializer(many=True, read_only=True)

    class Meta:
        model = Pedido
        fields = [
            'id', 'numero_pedido', 'cliente_nombre', 'cliente_cif', 
            'fecha_pedido', 'estado', 'direccion_envio', 'documento', 
            'created_at', 'updated_at', 'lineas'
        ]

    def create(self, validated_data):
        lineas_data = validated_data.pop('lineas')
        pedido = Pedido.objects.create(**validated_data)
        pedido.lineas.set(lineas_data)
        return pedido

    def update(self, instance, validated_data):
        lineas_data = validated_data.pop('lineas')
        instance = super().update(instance, validated_data)
        instance.lineas.set(lineas_data)
        return instance
