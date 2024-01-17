from rest_framework import viewsets
from rest_framework.generics import CreateAPIView

from .serializer import LoginUserSerializers, RegisterSerializer
from ...models import User
from rest_framework.decorators import action
from django.contrib.auth import login, logout
from rest_framework.response import Response
from rest_framework import status


class AccountModelviewset(viewsets.ModelViewSet):
    """
        this is ModelviewSet for loginuser ,logout user ,Register
    """
    serializer_class = LoginUserSerializers
    queryset = User.objects.all()

    @action(methods=['post'], detail=False)
    def login(self, request):
        """
            this is login user
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data.get('user')
            if user is not None:
                login(request, user)
                return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=False)
    def logout(self, request):
        """
               this is logout user
        """
        logout(request)
        return Response('Successfully logged out', status=status.HTTP_200_OK)


class RegisterViewSet(CreateAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            user = User.objects.create(email=email)
            user.set_password(password)
            user.save()
            return Response('Register user is successfully', status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
