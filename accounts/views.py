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


class UserCreateAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)


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
