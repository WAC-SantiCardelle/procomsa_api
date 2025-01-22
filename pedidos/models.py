from django.db import models

class Pedido(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('validado', 'Validado'),
        ('procesado', 'Procesado'), 
        ('cancelado', 'Cancelado')
    ]

    numero_pedido = models.CharField(max_length=30, unique=True)
    cliente_nombre = models.CharField(max_length=100, verbose_name="Nombre del Cliente")
    cliente_cif = models.CharField(max_length=12, verbose_name="CIF")
    fecha_pedido = models.DateField(verbose_name="Fecha del Pedido")
    estado = models.CharField(
        max_length=10, 
        choices=ESTADO_CHOICES,
        default='pendiente',
        verbose_name="Estado"
    )
    direccion_envio = models.TextField(max_length=200, verbose_name="Dirección de Envío")
    documento = models.FileField(upload_to='pedidos/documents/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Última Actualización")

    class Meta:
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"
        ordering = ['-fecha_pedido']

    def __str__(self):
        return f'Pedido {self.numero_pedido} ({self.estado}) - {self.cliente_nombre}'

    
class LineaPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='lineas')
    producto = models.CharField(max_length=100, verbose_name="Producto")
    referencia = models.CharField(max_length=20, verbose_name="Referencia")
    cantidad = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Última Actualización")
    
    def __str__(self):
        return f'Linea {self.id}: {self.producto} x {self.cantidad} (Ref: {self.referencia})'


