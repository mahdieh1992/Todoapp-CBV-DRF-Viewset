<<<<<<< HEAD
from django.views.static import serve
from rest_framework.generics import GenericAPIView
from .serializer import AccountSerializers, Loginserializer
=======
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView, UpdateAPIView, GenericAPIView
from .serializer import LoginUserSerializers, RegisterSerializer, ProfileSerializer, ChangePasswordSerializer
from ...models import User, UserDetail
from rest_framework.decorators import action
from django.contrib.auth import login, logout
>>>>>>> master
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import permissions
from rest_framework import status
<<<<<<< HEAD
from django.contrib.auth import login, logout
from ...models import User
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializer import TokenJwtSerializer
=======
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from mail_templated import EmailMessage, send_mail
from rest_framework_simplejwt.tokens import RefreshToken
from .utily import EmailThreading
>>>>>>> master


class RegistrationGAPIView(GenericAPIView):
    """
        this is Register user and show data According to desired field
    """
    serializer_class = AccountSerializers

    def post(self, request, *args, **kwargs):
        """
            this is register user
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            email = serializer.validated_data['email']
<<<<<<< HEAD

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


=======
            password = serializer.validated_data['password']
            user = User.objects.create(email=email, is_staff=True, is_superuser=True)
            user.set_password(password)
            user.save()
            # find user trgisterd for create token
            user_obj = get_object_or_404(User, email=email)
            # create token for user registerd
            tokecreate = self.get_tokens_for_user(user_obj)
            # send email contain token to new userr
            emailuser = EmailMessage('email/Activation.tp1', {'token': tokecreate}, 'mohamadimahdieh70@gmil.com',
                                     [email])
            # send email with threading for increase speed
            email_object = EmailThreading(emailuser)
            email_object.start()
            return Response('Register user is successfully so for  finally register we sended a code for user',
                            status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_tokens_for_user(self, user):
        """
            function create token manually with jwt
        """
        token = RefreshToken.for_user(user)
        return str(token)


class ProfileApiView(RetrieveUpdateAPIView):
    """
        this is for view detail of user and update  user information
    """
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]
    queryset = UserDetail.objects.all()

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, User_id=self.request.user)
        return obj


class ChangePasswordApi(GenericAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def put(self, request, *args, **kwargs):
        object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            password = serializer.data.get('NewPassword')
            object.set_password(password)
            object.save()
            return Response({'data': 'Change pass word successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ActivationUserApi(APIView):
    def get(self):
        pass


class SendMailApi(APIView):
    def get(self, request, *args, **kwargs):
        email = EmailMessage('email/hello.tp1', {'user': 'mahdieh'}, 'mohamadimahdieh70@gmil.com',
                             ['ebrahimi.7diamonds@gmail.com'])
        emailthread = EmailThreading(email)
        emailthread.start()
        return Response('Email send successfully', status=status.HTTP_200_OK)
>>>>>>> master
