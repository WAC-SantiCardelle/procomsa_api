from rest_framework import viewsets, status
from rest_framework.pagination import PageNumberPagination
from django_filters import rest_framework as filters
from .models import OrderInfo, OrderData, StatusType
from .serializers import OrderInfoSerializer, OrderDataSerializer, StatusTypeSerializer
from rest_framework.response import Response
from rest_framework.decorators import action
from .utils import generate_txt # importar la funcion desde utils

class CustomPagination(PageNumberPagination):
    page_size = 200
    page_size_query_param = 'page_size'
    max_page_size = 300

class OrderInfoFilter(filters.FilterSet):
    fecha_inicio = filters.DateFilter(field_name='order_date', lookup_expr='gte')
    fecha_fin = filters.DateFilter(field_name='order_date', lookup_expr='lte')
    mod_inicio = filters.DateFilter(field_name='updated_at', lookup_expr='gte')  # Nuevo filtro
    mod_fin = filters.DateFilter(field_name='updated_at', lookup_expr='lte')  # Nuevo filtro
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
    """
    ViewSet para manejar las operaciones CRUD de los pedidos.

    - **GET**: Listar todos los pedidos.
    - **POST**: Crear un nuevo pedido.
    - **GET {id}**: Obtener los detalles de un pedido específico.
    - **PUT {id}**: Actualizar un pedido específico.
    - **DELETE {id}**: Eliminar un pedido específico.
    """
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
        """
        Actualiza un pedido específico.

        Si se envía un `status_id`, se convierte a un objeto de estado.
        """
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
    
    @action(detail=True, methods=['put'], url_path='generate-txt')
    def generate_txt_update(self, request, pk=None):
        """
        Endpoint para actualizar un pedido y generar un archivo TXT.
        PUT /api/pedidos/{id}/generate-txt/
        """
        try:
            # Obteenr la instancia del pedido
            instance = self.get_object()

            # Actializar el pedido usando el metodo update existente
            response = self.update(request, pk=pk)  

            if response.status_code == status.HTTP_200_OK:
                # Si la actualizacion ha sido correcta, generar el txt
                try:
                     generate_txt(instance) # Usar la función importada
                     return Response({
                          'message': 'Pedido actualizado y archivo generado con exito',
                          'data': response.data
                     })
                except Exception as e:
                     # Si falla la generación del TXT, cambiar el estado a 3 'revision'
                    try:
                        error_status = StatusType.objects.get(id_status_type=3)
                        instance.status = error_status
                        instance.save()
                        return Response({
                            'message': f'Pedido actualizado pero error al generar TXT: {str(e)}. Estado cambiado a revision.',
                            'data': self.get_serializer(instance).data
                        }, status=status.HTTP_206_PARTIAL_CONTENT)
                    except StatusType.DoesNotExist:
                        return Response({
                            'message': f'Error al generar TXT y al cambiar estado: Status 3 no existe',
                            'data': response.data
                        }, status=status.HTTP_206_PARTIAL_CONTENT)
                    except Exception as status_error:
                        return Response({
                            'message': f'Error al generar TXT y al cambiar estado: {str(status_error)}',
                            'data': response.data
                        }, status=status.HTTP_206_PARTIAL_CONTENT)
                
            return response
        
        except Exception as e:
            return Response({
                'error': f'Error al procesar la solicitud: {str(e)}'
            }, status=status.HTTP_400_BAD_REQUEST)
                    

class OrderDataViewSet(viewsets.ModelViewSet):
    """
    ViewSet para manejar las operaciones CRUD de las líneas de pedido.

    - **GET**: Listar todas las líneas de pedido.
    - **POST**: Crear una nueva línea de pedido.
    - **GET {id}**: Obtener los detalles de una línea de pedido específica.
    - **PUT {id}**: Actualizar una línea de pedido específica.
    - **DELETE {id}**: Eliminar una línea de pedido específica.
    """
    queryset = OrderData.objects.all()
    serializer_class = OrderDataSerializer

class StatusTypeViewSet(viewsets.ModelViewSet):
    """
    ViewSet para manejar las operaciones CRUD de los tipos de estado.

    - **GET**: Listar todos los tipos de estado.
    - **POST**: Crear un nuevo tipo de estado.
    - **GET {id}**: Obtener los detalles de un tipo de estado específico.
    - **PUT {id}**: Actualizar un tipo de estado específico.
    - **DELETE {id}**: Eliminar un tipo de estado específico.
    """
    queryset = StatusType.objects.all()
    serializer_class = StatusTypeSerializer
