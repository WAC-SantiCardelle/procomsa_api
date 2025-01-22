from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from django_filters import rest_framework as filters
from .models import Pedido, LineaPedido
from .serializers import PedidoSerializer, LineaPedidoSerializer

class CustomPagination(PageNumberPagination):
    page_size = 8
    page_size_query_param = 'page_size'
    max_page_size = 100

class PedidoFilter(filters.FilterSet):
    fecha_inicio = filters.DateFilter(field_name='fecha_pedido', lookup_expr='gte')
    fecha_fin = filters.DateFilter(field_name='fecha_pedido', lookup_expr='lte')
    
    class Meta:
        model = Pedido
        fields = ['estado']

class PedidoViewSet(viewsets.ModelViewSet):
    queryset = Pedido.objects.all().order_by('-fecha_pedido')
    serializer_class = PedidoSerializer
    pagination_class = CustomPagination
    filterset_class = PedidoFilter
    filter_backends = (filters.DjangoFilterBackend,)

class LineaPedidoViewSet(viewsets.ModelViewSet):
    queryset = LineaPedido.objects.all()
    serializer_class = LineaPedidoSerializer
