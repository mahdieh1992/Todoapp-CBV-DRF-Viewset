from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import ProfileApiView, SendMailApi, ChangePasswordApi, SendVerifyUserApi, RegistrationGAPIView, \
    LoginApiView, LogoutApi, ResendVerifyUserApi, SendResetPasswordEmail, ResetPassword
from rest_framework.authtoken.views import obtain_auth_token
from .views import TokenViewJwt
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

app_name = 'AccountApi'

router = DefaultRouter()

urlpatterns = [
    path('account/register/', RegistrationGAPIView.as_view(), name='register'),
    path('account/confirm/<str:token>', SendVerifyUserApi.as_view(), name='confirm'),
    path('account/ResendVerify/', ResendVerifyUserApi.as_view(), name='ResendVerify'),
    path('account/profile/', ProfileApiView.as_view(), name='profile'),
    path('account/ChangePassword/', ChangePasswordApi.as_view(), name='ChangePass'),
    path('account/SendResetPasswordEmail/', SendResetPasswordEmail.as_view(), name='SendResetPasswordEmail'),
    path('account/ResetPasword/<str:token>', ResetPassword.as_view(), name='ResetPassword'),
    path('testSendEmail/', SendMailApi.as_view(), name='SendMail'),
    path('registration/', RegistrationGAPIView.as_view(), name='registration'),
    path('login/', LoginApiView.as_view(), name='login'),
    path('logout/', LogoutApi.as_view(), name='logout'),
    path('api/token/', TokenViewJwt.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify')
]

urlpatterns += router.urls
