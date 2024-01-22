from django.views.static import serve
from rest_framework.generics import GenericAPIView
from .serializer import AccountSerializers, Loginserializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import permissions
from rest_framework import status
from django.contrib.auth import login, logout
from ...models import User
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializer import TokenJwtSerializer


class RegistrationGAPIView(GenericAPIView):
    """
        this is Register user and show data According to desired field
    """
    serializer_class = AccountSerializers

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            email = serializer.validated_data['email']

            data = {
                'email': email
            }
            return Response(data=data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginApiView(GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = Loginserializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            login(request, user)
            return Response({'Detail': 'welcome dear user',
                             'toke': token.key
                             }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutApi(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        self.request.user.auth_token.delete()
        logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)


class TokenViewJwt(TokenObtainPairView):
    serializer_class = TokenJwtSerializer


