from django.urls import path
from . import views


urlpatterns = [
    path("register/", views.UserCreateAPIView.as_view(), name="user-create"),
    path(
        "verify-email/<uuid:user_id>/",
        views.VerifyEmailView.as_view(),
        name="verify-email",
    ),
    # path("d-rest-auth/login/", views.CustomAuthToken.as_view(), name="login"),
    path("users/", views.UserListAPIView.as_view(), name="user-list"),
    path("user-details/", views.UserDetailsView.as_view(), name="user-details"),
    path(
        "uservisits/statistics/",
        views.UserVisitStatistics.as_view(),
        name="user-visit-statistics",
    ),
]
