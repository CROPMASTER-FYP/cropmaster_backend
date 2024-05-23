from django.urls import path
from .views import MonthlyOrderStats, ProductViewSet, OrderViewSet, WeeklyOrderStats

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
    path(
        "orders/buyer_orders/",
        OrderViewSet.as_view({"get": "buyer_orders"}),
        name="buyer-orders",
    ),
    path(
        "orders/farmer_orders/",
        OrderViewSet.as_view({"get": "farmer_orders"}),
        name="farmer-orders",
    ),
    path(
        "orders/<uuid:pk>/mark_as_processed/",
        OrderViewSet.as_view({"put": "mark_as_processed"}),
        name="order-mark-processed",
    ),
    path('orders/stats/weekly/', WeeklyOrderStats.as_view(), name='weekly-stats'),
    path('orders/stats/monthly/', MonthlyOrderStats.as_view(), name='monthly-stats'),
]

