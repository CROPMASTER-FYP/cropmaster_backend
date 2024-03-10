from django.urls import path
from .views import ProductViewSet, OrderViewSet

urlpatterns = [
    path(
        "products/",
        ProductViewSet.as_view({"get": "list", "post": "create"}),
        name="product-list",
    ),
    path(
        "products/<uuid:pk>/",
        ProductViewSet.as_view(
            {
                "get": "retrieve",
                "put": "update",
                "patch": "partial_update",
                "delete": "destroy",
            }
        ),
        name="product-detail",
    ),
    path(
        "orders/",
        OrderViewSet.as_view({"get": "list", "post": "create"}),
        name="order-list",
    ),
    path(
        "orders/<uuid:pk>/",
        OrderViewSet.as_view(
            {
                "get": "retrieve",
                "put": "update",
                "patch": "partial_update",
                "delete": "destroy",
            }
        ),
        name="order-detail",
    ),
]
