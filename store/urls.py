from django.urls import path, include
from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()
router.register('products', views.ProductViewSet, basename='products')
router.register('collections', views.CollectionViewSet)
router.register('carts', views.CartViewSet)
router.register('customers', views.CustomerViewSet)

products_routers = routers.NestedDefaultRouter(router, 'products', lookup='product')
products_routers.register('reviews', views.ReviewViewSet, basename='product-review')

cart_routers = routers.NestedDefaultRouter(router, 'carts', lookup='cart')
cart_routers.register('items', views.CartItemViewSet, basename='cart-items-detail')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(products_routers.urls)),
    path('', include(cart_routers.urls))
]
