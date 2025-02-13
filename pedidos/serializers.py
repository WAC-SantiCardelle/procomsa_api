from rest_framework import serializers
from .models import OrderInfo, OrderData, StatusType

# Serializer para StatusType (si es necesario incluir detalles completos del estado)
class StatusTypeSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo StatusType.

    - **Campos de entrada**: 
        - `id_status_type`: ID del estado (solo lectura).
        - `status_name`: Nombre del estado (requerido).

    - **Campos de salida**: 
        - `id_status_type`
        - `status_name`
    """
    class Meta:
        model = StatusType
        fields = ['id_status_type', 'status_name']

# Serializer para OrderData
class OrderDataSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo OrderData.

    - **Campos de entrada**: 
        - `id`: ID de la línea de pedido (solo lectura).
        - `product_code`: Código del producto (requerido).
        - `quantity`: Cantidad (requerido).
        - `description`: Descripción del producto (requerido).

    - **Campos de salida**: 
        - `id_product`
        - `product_code`
        - `quantity`
        - `description`
    """
    class Meta:
        model = OrderData
        fields = ['id_product', 'product_code', 'quantity', 'description']

# Serializer para OrderInfo (antes Pedido)
class OrderInfoSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo OrderInfo.

    - **Campos de entrada**: 
        - `id_order`: ID del pedido (solo lectura).
        - `order_number`: Número de pedido (requerido).
        - `order_date`: Fecha del pedido (requerido).
        - `client_name`: Nombre del cliente (requerido).
        - `notes`: Observaciones (opcional).
        - `cif`: CIF del cliente (requerido).
        - `status`: Estado del pedido (solo lectura).
        - `status_id`: ID del estado (requerido).
        - `shipping_address`: Dirección de envío (requerido).
        - `file_path`: Ruta del archivo (opcional).
        - `lines`: Líneas de pedido (requerido).

    - **Campos de salida**: 
        - `id_order`
        - `order_number`
        - `order_date`
        - `client_name`
        - `notes`
        - `cif`
        - `status`
        - `status_id`
        - `shipping_address`
        - `file_path`
        - `created_at`: Fecha de creación (solo lectura).
        - `updated_at`: Última actualización (solo lectura).
        - `lines`: Detalles de las líneas de pedido.
    """
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
            'id_order', 'order_number', 'order_date', 'client_name', 'notes', 'cif', 
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
