from django.contrib import admin
from .models import Pedido, LineaPedido

class LineaPedidoInline(admin.TabularInline):
    model = LineaPedido
    extra = 1
    fields = ['producto', 'referencia', 'cantidad']

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ['numero_pedido', 'cliente_nombre', 'fecha_pedido', 'estado']
    list_filter = ['estado', 'fecha_pedido']
    search_fields = ['numero_pedido', 'cliente_nombre', 'cliente_cif']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [LineaPedidoInline]
    
    fieldsets = (
        ('Información del Cliente', {
            'fields': ('numero_pedido', 'cliente_nombre', 'cliente_cif')
        }),
        ('Detalles del Pedido', {
            'fields': ('fecha_pedido', 'estado', 'direccion_envio')
        }),
        ('Documentación', {
            'fields': ('documento',)
        }),
        ('Información del Sistema', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    ordering = ['-fecha_pedido']

@admin.register(LineaPedido)
class LineaPedidoAdmin(admin.ModelAdmin):
    list_display = ['pedido', 'producto', 'referencia', 'cantidad']
    search_fields = ['producto', 'referencia']
    list_filter = ['created_at']