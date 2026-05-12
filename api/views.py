from django.shortcuts import render , get_object_or_404
from django.db.models import Max
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics
from .serializers import *
from .models import *


class ProductListAPIView(generics.ListAPIView):
    queryset= Product.objects.all()
    serializer_class =  ProductSerializer


class ProductRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_url_kwarg = 'product_id'

class OrderListAPIView(generics.ListAPIView):
    queryset = Order.objects.prefetch_related('items__product')
    serializer_class = OrderSerializer


class UserOrderListAPIView(generics.ListAPIView):
    queryset = Order.objects.prefetch_related('items__product')
    serializer_class = OrderSerializer
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(user=self.request.user)
    
    
@api_view(['GET'])
def product_info(request):
    products = Product.objects.all()
    serializer = ProductInfoSerializer({
        'products':products,
        'count':len(products),
        'max_price':products.aggregate(max_price=Max('price'))['max_price']
    })
    return Response(serializer.data)