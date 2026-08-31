from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Order
from .serializers import OrderSerializer
from .services import recommend_box


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    @action(detail=True, methods=["post"], url_path="recommend-box")
    def recommend_box_action(self, request, pk=None):
        order = self.get_object()

        selected_box = recommend_box(order.items.select_related("product").all())

        if selected_box is None:
            return Response(
                {
                    "message": "No suitable box found for this order."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        return Response(
            {
                "order_id": order.id,
                "recommended_box": {
                    "id": selected_box.id,
                    "name": selected_box.name,
                    "cost": selected_box.cost,
                    "max_weight": selected_box.max_weight,
                }
            },
            status=status.HTTP_200_OK
        )