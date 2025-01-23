from rest_framework import serializers
from .models import Pedido, LineaPedido

class LineaPedidoSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = LineaPedido
        fields = ['id', 'producto', 'referencia', 'cantidad']

class PedidoSerializer(serializers.ModelSerializer):
    lineas = LineaPedidoSerializer(many=True)

    class Meta:
        model = Pedido
        fields = [
            'id', 'numero_pedido', 'cliente_nombre', 'cliente_cif', 
            'fecha_pedido', 'estado', 'direccion_envio', 'documento', 
            'created_at', 'updated_at', 'lineas'
        ]

    def update(self, instance, validated_data):
        lineas_data = validated_data.pop('lineas', [])
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        lineas_actualizadas = []
        
        for linea_data in lineas_data:
            linea_id = linea_data.get('id', None)
            if linea_id:
                try:
                    linea = LineaPedido.objects.get(id=linea_id, pedido=instance)
                    for key, value in linea_data.items():
                        setattr(linea, key, value)
                    linea.save()
                    lineas_actualizadas.append(linea)
                except LineaPedido.DoesNotExist:
                    linea = LineaPedido.objects.create(pedido=instance, **linea_data)
                    lineas_actualizadas.append(linea)
            else:
                linea = LineaPedido.objects.create(pedido=instance, **linea_data)
                lineas_actualizadas.append(linea)

        instance.lineas.exclude(id__in=[l.id for l in lineas_actualizadas]).delete()

        return instance

    def create(self, validated_data):
        lineas_data = validated_data.pop('lineas', [])
        pedido = Pedido.objects.create(**validated_data)
        
        for linea_data in lineas_data:
            LineaPedido.objects.create(pedido=pedido, **linea_data)
            
        return pedido
