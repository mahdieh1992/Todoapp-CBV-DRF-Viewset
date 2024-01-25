from django.urls import path
<<<<<<< HEAD
from .views import RegistrationGAPIView,LoginApiView,LogoutApi
from rest_framework.authtoken.views import obtain_auth_token
from .views import TokenViewJwt
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
app_name = 'AccountApi'
urlpatterns = [
=======
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
>>>>>>> master

    path('registration/', RegistrationGAPIView.as_view(), name='registration'),
    path('login/', LoginApiView.as_view(), name='login'),
    path('logout/',LogoutApi.as_view(), name='logout'),
    path('api/token/', TokenViewJwt.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
