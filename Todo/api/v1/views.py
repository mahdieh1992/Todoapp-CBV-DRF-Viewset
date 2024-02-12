from .serializer import TodoSerializer, CitySerializer
from ...models import Todo
from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from .pagination import TodolistPage
from rest_framework import status
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie, vary_on_headers


class TodoListModelViewSet(viewsets.ModelViewSet):
    """
    this is ModelViewSet for View and Create Todo
    """

    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [OrderingFilter, SearchFilter, DjangoFilterBackend]
    filterset_fields = {"Title": ["in"]}
    search_fields = ["Title"]
    ordering_fields = ["CreateDate"]
    pagination_class = TodolistPage

    def list(self, request, *args, **kwargs):
        """
        this is ModelViewSet for View Todo
        """
        queryset = self.filter_queryset(
            self.get_queryset().filter(user=self.request.user)
        )
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        """
        this is ModelViewSet for Save Create Todo
        """
        serializer.save(user=self.request.user)


class TodoDetailGenericViewSet(generics.RetrieveUpdateDestroyAPIView):
    """
    this is for TodoDetail
    """

    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = self.queryset.filter(user=self.request.user)
        return queryset


class WeatherApiView(generics.GenericAPIView):
    serializer_class = CitySerializer

    @method_decorator(cache_page(60*20))
    @method_decorator(vary_on_cookie)
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            city=serializer.data.get('cityname')
            city_weather = serializer.validated_data['city_weather']
            weather = {
                'city': city,
                'temperature': str(city_weather['main']['temp']),
                'description': str(city_weather['weather'][0]['description']),
                'icon': str(city_weather['weather'][0]['icon']),
                'temperature_max': str(city_weather['main']['temp_max']),
                'temperature_min': str(city_weather['main']['temp_min']),
                'feelslike_weather': str(city_weather['main']['feels_like'])

            }
            return Response(weather,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)