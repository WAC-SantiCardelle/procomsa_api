from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from django_filters import rest_framework as filters
from .models import OrderInfo, OrderData, StatusType
from .serializers import OrderInfoSerializer, OrderDataSerializer, StatusTypeSerializer
from rest_framework.response import Response

class CustomPagination(PageNumberPagination):
    page_size = 8
    page_size_query_param = 'page_size'
    max_page_size = 100

class OrderInfoFilter(filters.FilterSet):
    fecha_inicio = filters.DateFilter(field_name='order_date', lookup_expr='gte')
    fecha_fin = filters.DateFilter(field_name='order_date', lookup_expr='lte')
    status = filters.ModelMultipleChoiceFilter(
        queryset=StatusType.objects.all(),
        field_name='status',
        to_field_name='id_status_type',
        conjoined=False  # Permite OR en lugar de AND
    )
    
    class Meta:
        model = OrderInfo
        fields = ['status']

class OrderInfoViewSet(viewsets.ModelViewSet):
    queryset = OrderInfo.objects.all().select_related('status').prefetch_related('lines')
    serializer_class = OrderInfoSerializer
    pagination_class = CustomPagination
    filterset_class = OrderInfoFilter
    filter_backends = (filters.DjangoFilterBackend,)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        
        # Si se envía un status_id, convertirlo a status
        if 'status' in request.data and isinstance(request.data['status'], (int, str)):
            try:
                status_id = int(request.data['status'])
                request.data['status'] = {'id_status_type': status_id}
            except (ValueError, TypeError):
                pass

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)

class OrderDataViewSet(viewsets.ModelViewSet):
    queryset = OrderData.objects.all()
    serializer_class = OrderDataSerializer

class StatusTypeViewSet(viewsets.ModelViewSet):
    queryset = StatusType.objects.all()
    serializer_class = StatusTypeSerializer
