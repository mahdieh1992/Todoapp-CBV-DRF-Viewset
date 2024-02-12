from rest_framework.generics import RetrieveUpdateAPIView, GenericAPIView
from Core import settings
from .serializer import (
    Loginserializer,
    RegisterSerializer,
    ProfileSerializer,
    ChangePasswordSerializer,
    SendResetPasswordSerializer,
    ResendVerifySerializer,
    ResetPasswordSerializer,
)
from accounts.tasks import send_email
from ...models import UserDetail
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


def get_tokens_for_user(user):
    """
    function create token manually with jwt
    """
    refresh = RefreshToken.for_user(user)
    return str(refresh.access_token)


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
            email = serializer.validated_data["email"]
            password = serializer.validated_data["password"]
            user = User.objects.create(
                email=email, is_staff=True, is_superuser=True
            )
            user.set_password(password)
            user.save()
            # find user trgisterd for create token
            user_obj = get_object_or_404(User, email=email)
            # create token for user registerd
            tokecreate = get_tokens_for_user(user_obj)
            # send email contain token to new userr
            # send email with threading for increase speed
            send_email.delay(
                "email/Confirm.tp1",
                {"token": tokecreate},
                "mohamadimahdieh70@gmil.com",
                [email],
            )
            return Response(
                "we sending email contain token", status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SendVerifyUserApi(APIView):
    """
    this is to confirm registration user
    """

    def get(self, request, token, *args, **kwargs):
        try:
            # try decode toke to get userid
            Payload = jwt.decode(
                token, key=settings.SECRET_KEY, algorithms=["HS256"]
            )
            user_object = get_object_or_404(User, id=Payload["user_id"])
            if user_object.is_verified:
                return Response(
                    {"detail": "user is_verified"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            else:
                user_object.is_verified = True
                user_object.save()
                return Response(
                    {"detail": "user is_verified successfully"},
                    status=status.HTTP_200_OK,
                )
        # except if token improperly
        except jwt.exceptions.DecodeError as e:
            return Response(
                {"Error": "invalid token"}, status=status.HTTP_400_BAD_REQUEST
            )
        #  except while the toke expired
        except jwt.exceptions.ExpiredSignatureError as e:
            return Response(
                {"Error": "token expired"}, status=status.HTTP_400_BAD_REQUEST
            )


class ResendVerifyUserApi(GenericAPIView):
    """
    if token expired we resend a new token to user for confirm account
    """

    serializer_class = ResendVerifySerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        # receate token and send to emails user to confirm
        token = get_tokens_for_user(user)
        email = EmailMessage(
            "email/Confirm.tp1",
            {"token": token},
            "mohamadimahdieh70@gmil.com",
            [user.email],
        )
        emailthread = EmailThreading(email)
        emailthread.start()
        return Response(
            {"detail": "we sending a confirm code your email"},
            status=status.HTTP_200_OK,
        )


class LoginApiView(GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = Loginserializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            token, created = Token.objects.get_or_create(user=user)
            login(request, user)
            return Response(
                {"Detail": "welcome dear user", "toke": token.key},
                status=status.HTTP_200_OK,
            )

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
    """
    this is view for change password user
    """

    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def put(self, request, *args, **kwargs):
        object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            password = serializer.data.get("NewPassword")
            object.set_password(password)
            object.save()
            return Response(
                {"data": "Change pass word successfully"},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SendResetPasswordEmail(GenericAPIView):
    """
    this is generate token for Request Reset Password user
    """

    serializer_class = SendResetPasswordSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            # genarate token if user is exists
            token = get_tokens_for_user(user)
            # send toke to email user
            email = EmailMessage(
                "email/RequestResetPassword.tp1",
                {"token": token},
                "mohamadimahdieh70@gmil.com",
                [user.email],
            )
            emailthread = EmailThreading(email)
            emailthread.start()
            return Response(
                {"detail": "we sending for you a email contain code"},
                status=status.HTTP_200_OK,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResetPassword(GenericAPIView):
    """
    this is a GenericAPIView for reset password user
    it performed if the token entered is correct
    """

    serializer_class = ResetPasswordSerializer

    def post(self, request, token, *args, **kwargs):

        try:
            # try for decode token and get userid
            payload = jwt.decode(
                token, key=settings.SECRET_KEY, algorithms=["HS256"]
            )
            user = get_object_or_404(User, id=payload["user_id"])
            # if user exists and serializer
            # validated change password is complete
            if user:
                serializer = self.get_serializer(data=request.data)
                if serializer.is_valid():
                    password = serializer.data.get("NewPassword")
                    user.set_password(password)
                    user.save()
                    return Response(
                        {"detail": "change password is complete"},
                        status=status.HTTP_200_OK,
                    )
                return Response(
                    serializer.errors, status=status.HTTP_400_BAD_REQUEST
                )
        except jwt.exceptions.DecodeError as e:
            return Response(
                {"detail": "token is not valid"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except jwt.exceptions.ExpiredSignatureError as e:
            return Response(
                {"detail": "token is expired"},
                status=status.HTTP_408_REQUEST_TIMEOUT,
            )


class SendMailApi(APIView):
    def get(self, request, *args, **kwargs):
        email = EmailMessage(
            "email/hello.tp1",
            {"user": "mahdieh"},
            "mohamadimahdieh70@gmil.com",
            ["ebrahimi.7diamonds@gmail.com"],
        )
        emailthread = EmailThreading(email)
        emailthread.start()
        return Response("Email send successfully", status=status.HTTP_200_OK)
