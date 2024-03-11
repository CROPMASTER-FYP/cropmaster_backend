from django.urls import path
from .views import (
    ExtensionOfficerMessagesViewSet,
    ExtensionOfficerViewSet,
    MessageViewSet,
    ResponseViewSet,
)


urlpatterns = [
    path(
        "extension-officer/",
        ExtensionOfficerViewSet.as_view({"get": "list"}),
    ),
    path(
        "extension-officer/<uuid:extension_officer_id>/messages/",
        ExtensionOfficerMessagesViewSet.as_view({"get": "list"}),
    ),
    path(
        "extension-officer/<uuid:pk>/",
        ExtensionOfficerViewSet.as_view(
            {"get": "retrieve", "put": "update", "delete": "destroy"}
        ),
    ),
    path(
        "messages/",
        MessageViewSet.as_view({"get": "list", "post": "create"}),
        name="message-list",
    ),
    path(
        "messages/<int:pk>/",
        MessageViewSet.as_view(
            {"get": "retrieve", "put": "update", "delete": "destroy"}
        ),
        name="message-detail",
    ),
    path(
        "messages/<int:message_id>/responses/",
        ResponseViewSet.as_view({"get": "list", "post": "create"}),
        name="response-list",
    ),
]
