from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import TodoListModelViewSet, TodoDetailGenericViewSet,WeatherApiView


app_name = "TodoApi"

router = DefaultRouter()
router.register("Todo", TodoListModelViewSet, basename="Todo")

urlpatterns = [
    path(
        "TodoDetail/<int:pk>",
        TodoDetailGenericViewSet.as_view(),
        name="TodoDetail",
    ),
    path("Weather/",WeatherApiView.as_view(),name="Weather")
]

urlpatterns += router.urls
