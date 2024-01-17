from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import AccountModelviewset,RegisterViewSet

router = DefaultRouter()
router.register('account', AccountModelviewset, basename='account')

urlpatterns = [
    path('account/register/',RegisterViewSet.as_view(),name='register')

]
urlpatterns += router.urls
