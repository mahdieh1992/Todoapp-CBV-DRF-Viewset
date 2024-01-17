from .serializer import TodoSerializer
from ...models import Todo
from rest_framework import viewsets,generics
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from .pagination import TodolistPage


class TodoListModelViewSet(viewsets.ModelViewSet):
    """
        this is ModelViewSet for View and Create Todo
    """
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [OrderingFilter, SearchFilter,DjangoFilterBackend]
    filterset_fields={
        'Title':['in']
    }
    search_fields = ["Title"]
    ordering_fields = ['CreateDate']
    pagination_class = TodolistPage

    def list(self, request, *args, **kwargs):
        """
            this is ModelViewSet for View Todo
        """
        queryset = self.filter_queryset(self.get_queryset().filter(user=self.request.user))
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
        queryset=self.queryset.filter(user=self.request.user)
        return queryset

















