from django.urls import path
from .views import ExtensionOfficerViewSet, MessageViewSet


urlpatterns = [
    path(
        "extension-officer/",
        ExtensionOfficerViewSet.as_view({"get": "list"}),
    ),
    path(
        "extension-officer/<uuid:pk>/",
        ExtensionOfficerViewSet.as_view(
            {"get": "retrieve", "put": "update", "delete": "destroy"}
        ),
    ),
    path("message/", MessageViewSet.as_view({"get": "list", "post": "create"})),
    path(
        "message/<int:pk>/",
        MessageViewSet.as_view(
            {"get": "retrieve", "put": "update", "delete": "destroy"}
        ),
    ),
]
