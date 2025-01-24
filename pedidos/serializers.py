from rest_framework import serializers
from .models import OrderInfo, OrderData, StatusType

# Serializer para StatusType (si es necesario incluir detalles completos del estado)
class StatusTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = StatusType
        fields = ['id_status_type', 'status_name']

# Serializer para OrderData
class OrderDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderData
        fields = ['id', 'product_code', 'quantity', 'description']

# Serializer para OrderInfo (antes Pedido)
class OrderInfoSerializer(serializers.ModelSerializer):
    status = StatusTypeSerializer(read_only=True)
    status_id = serializers.PrimaryKeyRelatedField(
        source='status',
        queryset=StatusType.objects.all(),
        write_only=True,
        required=False
    )
    lines = OrderDataSerializer(many=True)

    class Meta:
        model = OrderInfo
        fields = [
            'id_order', 'order_number', 'order_date', 'client_name', 'cif', 
            'status', 'status_id', 'shipping_address', 'file_path', 
            'created_at', 'updated_at', 'lines'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def update(self, instance, validated_data):
        lines_data = validated_data.pop('lines', [])
        status = validated_data.pop('status', None)
        
        # Actualizar campos del pedido
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        if status:
            instance.status = status
            
        instance.save()

        # Gestionar líneas
        instance.lines.all().delete()
        for line_data in lines_data:
            OrderData.objects.create(id_order=instance, **line_data)

        return instance

    def create(self, validated_data):
        lines_data = validated_data.pop('lines', [])
        status = validated_data.pop('status')
        
        order = OrderInfo.objects.create(**validated_data, status=status)
        
        for line_data in lines_data:
            OrderData.objects.create(id_order=order, **line_data)
            
        return order
