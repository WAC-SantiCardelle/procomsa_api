from django.db import models

class StatusType(models.Model):
    id_status_type = models.AutoField(primary_key=True, verbose_name="ID del Estado")
    status_name = models.CharField(max_length=20, unique=True, verbose_name="Estado")

    class Meta:
        db_table = 'status_type'  # Nombre personalizado de la tabla en la base de datos
        verbose_name = "Estado"
        verbose_name_plural = "Estados"
        ordering = ['status_name']
        
    def __str__(self):
        return self.status_name


class OrderInfo(models.Model):
    id_order = models.AutoField(primary_key=True, verbose_name="ID del Pedido")
    order_number = models.CharField(max_length=30, verbose_name="Número de Pedido")
    order_date = models.DateField(verbose_name="Fecha del Pedido")
    client_name = models.CharField(max_length=30, verbose_name="Nombre del Cliente")
    notes = models.TextField(max_length=255, verbose_name="Observaciones", blank=True, null=True)
    cif = models.CharField(max_length=15, verbose_name="CIF")
    status = models.ForeignKey(StatusType, on_delete=models.SET_NULL, db_column='status', null=True, verbose_name="Estado")
    shipping_address = models.CharField(max_length=50, verbose_name="Dirección de Envío")
    file_path = models.CharField(max_length=50, blank=True, null=True, verbose_name="Ruta del Archivo")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Última Actualización")

    class Meta:
        db_table = 'order_info'  # Nombre personalizado de la tabla
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"
        ordering = ['-order_date']

    def __str__(self):
        return f'Pedido {self.order_number} ({self.status}) - {self.client_name}'


class OrderData(models.Model):
    id_product = models.AutoField(primary_key=True, verbose_name="ID del Producto")
    id_order = models.ForeignKey(
        OrderInfo, on_delete=models.CASCADE,
        db_column='id_order',
        related_name='lines',
        verbose_name="Pedido")
    product_code = models.CharField(max_length=50, verbose_name="Referencia")
    quantity = models.FloatField(verbose_name="Cantidad")
    description = models.CharField(max_length=100, verbose_name="Producto")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Última Actualización")
    
    class Meta:
        db_table = 'order_data'  # Nombre personalizado de la tabla
        verbose_name = "Línea de Pedido"
        verbose_name_plural = "Líneas de Pedido"

    def __str__(self):
        return f'Linea {self.id}: {self.description} x {self.quantity} (Ref: {self.product_code})'
