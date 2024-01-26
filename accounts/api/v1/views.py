from rest_framework.generics import RetrieveUpdateAPIView, UpdateAPIView, GenericAPIView

from Core import settings
from .serializer import Loginserializer, RegisterSerializer, ProfileSerializer, ChangePasswordSerializer,ResendVerifySerializer
from ...models import User, UserDetail
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import status
from django.contrib.auth import login, logout
from ...models import User
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializer import TokenJwtSerializer
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from mail_templated import EmailMessage
from rest_framework_simplejwt.tokens import RefreshToken
from .utily import EmailThreading
import jwt


class RegistrationGAPIView(GenericAPIView):
    """
        this is Register user and show data According to desired field
    """
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        """
            this is register user
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            user = User.objects.create(email=email, is_staff=True, is_superuser=True)
            user.set_password(password)
            user.save()
            # find user trgisterd for create token
            user_obj = get_object_or_404(User, email=email)
            # create token for user registerd
            tokecreate = self.get_tokens_for_user(user_obj)
            # send email contain token to new userr
            emailuser = EmailMessage('email/Confirm.tp1', {'token': tokecreate}, 'mohamadimahdieh70@gmil.com',
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
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)


class SendVerifyUserApi(APIView):
    """
        this is to confirm registration user
    """
    def get(self,request,token,*args,**kwargs):
        try:
            # try decode toke to get userid
            Payload = jwt.decode(token, key=settings.SECRET_KEY, algorithms=['HS256'])
            user_object = get_object_or_404(User, id=Payload['user_id'])
            if user_object.is_verified:
                return Response({'detail': 'user is_verified'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                user_object.is_verified = True
                user_object.save()
                return Response({'detail': 'user is_verified successfully'}, status=status.HTTP_200_OK)
        # except if token improperly
        except jwt.exceptions.DecodeError as e:
            return Response({'Error': 'invalid token'}, status=status.HTTP_400_BAD_REQUEST)
        #  except while the toke expired
        except jwt.exceptions.ExpiredSignatureError as e:
            return Response({'Error': 'token expired'}, status=status.HTTP_400_BAD_REQUEST)


class ResendVerifyUserApi(GenericAPIView):
    serializer_class = ResendVerifySerializer

    def post(self,request):
        serializer=self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user=serializer.validated_data['user']
        # receate token and send to emails user to confirm
        token = self.get_tokens_for_user(user)
        email = EmailMessage('email/Confirm.tp1',{'token':token}, 'mohamadimahdieh70@gmil.com',[user.email])
        emailthread=EmailThreading(email)
        emailthread.start()
        return Response({'detail':'we sending a confirm code your email'},status=status.HTTP_200_OK)

    def get_tokens_for_user(self, user):
        """
            function create token manually with jwt
        """
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)


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

class SendMailApi(APIView):
    def get(self, request, *args, **kwargs):
        email = EmailMessage('email/hello.tp1', {'user': 'mahdieh'}, 'mohamadimahdieh70@gmil.com',
                             ['ebrahimi.7diamonds@gmail.com'])
        emailthread = EmailThreading(email)
        emailthread.start()
        return Response('Email send successfully', status=status.HTTP_200_OK)
