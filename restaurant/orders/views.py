from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderItemSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    http_method_names = ['get', 'post', 'put', 'delete']


    @action(detail=True, methods=['get'])
    def update_status(self, request, pk=None):
        order = self.get_object()
        new_status = request.query_params.get('status')
        try: 
            order.update_status(new_status)
            return Response({'status': 'status updated'})
        except ValueError: 
            return Response({'error': 'invalid status'}, status=status.HTTP_400_BAD_REQUEST)
        
class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer

