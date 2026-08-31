from rest_framework import viewsets
from products.serializers import ProductSerializer
from products.models import Product

# Create your views here.
class ProductViewSet(viewsets.ModelViewSet):
    queryset=Product.objects.all()
    serializer_class=ProductSerializer
