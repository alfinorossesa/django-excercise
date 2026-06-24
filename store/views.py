from django.shortcuts import get_object_or_404
from django.db.models import Count
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import Product, Collection
from .serializer import ProductSerializer, CollectionSerializeer

# Create your views here.
class ProductList(ListCreateAPIView):
    queryset = Product.objects.select_related('collection').order_by('id')
    serializer_class = ProductSerializer

    def get_serializer_context(self):
        return {'request': self.request}

class ProductDetail(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def delete(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        if product.orderitems.count() > 1:
            return Response({'error': 'Product cant be deleted because asociated with order item.'} ,status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CollectionList(ListCreateAPIView):
    queryset = Collection.objects.annotate(products_count=Count('products')).order_by('id')
    serializer_class = CollectionSerializeer

class CollectionDetail(RetrieveUpdateDestroyAPIView):
    queryset = Collection.objects.annotate(products_count=Count('products'))
    serializer_class = CollectionSerializeer

    def delete(self, request, pk):
        collection = get_object_or_404(Collection.objects.annotate(products_count=Count('products')), pk=pk)
        if collection.products.count() > 1:
            return Response({'error': 'Collection cant be deleted because inclune one ore more product'})
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)