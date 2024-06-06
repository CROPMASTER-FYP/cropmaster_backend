from django.urls import path
from .views import (
    ExtensionOfficerMessagesViewSet,
    ExtensionOfficerViewSet,
    MessageViewSet,
    ResponseViewSet,
)


urlpatterns = [
    path("available-officers/", ExtensionOfficerViewSet.as_view({"get": "list"})),
    path(
        "extension-officer/<uuid:extension_officer_id>/messages/",
        ExtensionOfficerMessagesViewSet.as_view({"get": "list"}),
    ),
    path(
        "extension-officer/<uuid:pk>/",
        ExtensionOfficerViewSet.as_view(
            {"get": "retrieve"}
        ), #, "put": "update", "delete": "destroy"
    ),
    path(
        "extension-officer/<uuid:extension_officer_id>/send-message/",
        MessageViewSet.as_view({"post": "create"}),
        name="send-message-to-officer",
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
