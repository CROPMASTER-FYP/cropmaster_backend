from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from cropmaster.pagination import StandardResultsSetPagination
from .models import User, UserVisit
from .serializers import UserSerializer
from rest_framework.response import Response
from django.utils.timezone import now, timedelta
from rest_framework.views import APIView
from django.db.models.functions import TruncDate
from django.db.models import Count
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import CustomUserDetailsSerializer
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status


class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super(CustomAuthToken, self).post(request, *args, **kwargs)
        if "email_not_verified" in request.session:
            del request.session["email_not_verified"]
            return Response(
                {"error": "Please verify your email to continue."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        token = Token.objects.get(key=response.data["token"])
        user = token.user

        return Response(
            {
                "token": token.key,
                "user_id": user.pk,
                "email": user.email,
                "username": user.username,
            }
        )


# class VerifyEmailView(APIView):
#     permission_classes = (AllowAny,)

#     def get(self, request, user_id):
#         user = get_object_or_404(User, id=user_id)
#         user.is_email_verified = True
#         user.save()
#         return Response({"message": "Email verified successfully"}, status=status.HTTP_200_OK)


class VerifyEmailView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        user.is_email_verified = True
        user.save()
        return Response(
            {"message": "Email verified successfully"}, status=status.HTTP_200_OK
        )


class UserCreateAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response(
            {
                "message": "User registered successfully. Please check your email to verify your account.",
                "user": serializer.data,
            },
            status=status.HTTP_201_CREATED,
            headers=headers,
        )

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context

    # def perform_create(self, serializer):
    #     serializer.save(context={"request": self.request})

    def perform_create(self, serializer):
        serializer.save()


class UserListAPIView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = StandardResultsSetPagination
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ["username", "email"]


class UserVisitStatistics(APIView):

    def get(self, request, *args, **kwargs):
        days = int(request.query_params.get("days", 365))
        start_date = now() - timedelta(days=days)

        # Aggregate visits by date
        visits = (
            UserVisit.objects.filter(timestamp__gte=start_date)
            .annotate(date=TruncDate("timestamp"))
            .values("date")
            .annotate(count=Count("id"))
            .order_by("date")
        )

        # Prepare the data dictionary
        data = {str((start_date + timedelta(days=i)).date()): 0 for i in range(days)}
        for visit in visits:
            data[str(visit["date"])] = visit["count"]

        return Response(data)


class UserDetailsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = CustomUserDetailsSerializer(request.user)
        return Response(serializer.data)
