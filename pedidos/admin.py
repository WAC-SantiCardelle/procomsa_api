from django.contrib import admin
from .models import OrderInfo, OrderData, StatusType

# Inline para mostrar las líneas del pedido en el admin
class OrderDataInline(admin.TabularInline):
    model = OrderData
    extra = 1
    fields = ['product_code', 'quantity', 'description']  # Los campos relevantes

# Registro del modelo StatusType
@admin.register(StatusType)
class StatusTypeAdmin(admin.ModelAdmin):
    list_display = ['id_status_type', 'status_name']
    search_fields = ['status_name']
    list_filter = ['status_name']

# Registro del modelo OrderInfo (antes Pedido)
@admin.register(OrderInfo)
class OrderInfoAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'client_name', 'order_date', 'status']
    list_filter = ['status', 'order_date']
    search_fields = ['order_number', 'client_name', 'cif']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [OrderDataInline]  # Inline para las líneas de pedido
    
    fieldsets = (
        ('Información del Cliente', {
            'fields': ('order_number', 'client_name', 'cif')
        }),
        ('Detalles del Pedido', {
            'fields': ('order_date', 'status', 'shipping_address')
        }),
        ('Documentación', {
            'fields': ('file_path',)
        }),
        ('Información del Sistema', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    ordering = ['-order_date']

# Registro del modelo OrderData (antes LineaPedido)
@admin.register(OrderData)
class OrderDataAdmin(admin.ModelAdmin):
    list_display = ['id_order', 'product_code', 'quantity', 'description']
    search_fields = ['product_code', 'description']
    list_filter = ['created_at']
