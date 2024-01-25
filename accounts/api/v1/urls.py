from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import AccountModelviewset,RegisterViewSet,ProfileApiView,SendMailApi,ChangePasswordApi,ActivationUserApi

router = DefaultRouter()
router.register('account',AccountModelviewset, basename='account')

urlpatterns = [
    path('account/register/',RegisterViewSet.as_view(),name='register'),
    path('account/confirm/', ActivationUserApi.as_view(), name='confirm'),
    path('account/profile/',ProfileApiView.as_view(),name='profile'),
    path('account/ChangePassword/',ChangePasswordApi.as_view(),name='ChangePass'),
    path('testSendEmail/',SendMailApi.as_view(),name='SendMail')

]
urlpatterns += router.urls
