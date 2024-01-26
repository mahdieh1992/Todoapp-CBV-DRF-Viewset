from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from ...models import User, UserDetail
from django.contrib.auth import authenticate
from django.contrib.auth import password_validation as passvalidate
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404

class AccountSerializers(serializers.ModelSerializer):
    """
        this is serializer model for Register user
    """
    password = serializers.CharField(max_length=200, write_only=True, style={'input_type': 'password'})
    ConfirmPassword = serializers.CharField(max_length=200, write_only=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['email', 'password', 'ConfirmPassword']

    def validate(self, attrs):
        """
            evaluate input data according match password and confirmPassword
            evaluate password according The password should not be short
        """
        password = attrs.get('password')
        ConfirmPassword = attrs.get('ConfirmPassword')
        if password != ConfirmPassword:
            raise ValidationError({'password': "Doesn't match password and confirmpassword"}, code="password_not_match")
        try:
            validate_password(password)
        except ValidationError as e:
            raise ValidationError({'password': tuple(e.messages)}, code='password_too_short')

        return super(AccountSerializers, self).validate(attrs)

    def create(self, validated_data):
        """
             save data according desired items
        """
        validated_data.pop('ConfirmPassword')
        return User.objects.create(**validated_data)


class Loginserializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=200, write_only=True, style={'input_type': 'password'})

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        if email and password:
            user = authenticate(request=self.context.get('request'), email=email, password=password)
            if not user:
                raise serializers.ValidationError('wrong Email or password', code='Email_not_exists')
        else:
            raise serializers.ValidationError({'user': 'must be include email and password'},
                                              code='required_email_password')

        data['user'] = user
        return data


class TokenJwtSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        validated_data = super().validate(attrs)
        validated_data['email'] = self.user.email
        return validated_data


class RegisterSerializer(serializers.ModelSerializer):
    confirmPassword = serializers.CharField(max_length=255, style={'input_type': 'password'})
    password = serializers.CharField(max_length=255, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['email', 'password', 'confirmPassword']

    def validate(self, data):
        password = data.get('password')
        confirmPassword = data.get('confirmPassword')
        email = data.get('email')
        if password != confirmPassword:
            raise serializers.ValidationError('Not match password and Confirm password')
        if User.objects.filter(email=email, password=password).exists():
            raise serializers.ValidationError('User is exists')
        return data


class ResendVerifySerializer(serializers.Serializer):
    Email = serializers.CharField()

    def validate(self, data):
        email = data.get('Email')
        try:
            user =get_object_or_404(User,email=email)
            if user.is_verified:
                raise serializers.ValidationError({'detail':'Dear user your account is verified'}, code='ResendVerify')
        except ValidationError as e:
            raise serializers.ValidationError({'user':e.messages}, code='User_not_exists')
        data['user'] = user
        return data


class ProfileSerializer(serializers.ModelSerializer):
    email = serializers.CharField(read_only=True, source='User.email')

    class Meta:
        model = UserDetail
        fields = ['User_id', 'email', 'FirstName', 'LastName', 'Gender', 'NationalCode', 'Mobile']


class ChangePasswordSerializer(serializers.Serializer):
    OldPassword = serializers.CharField()
    NewPassword = serializers.CharField()
    ConfirmPassword = serializers.CharField()

    def validate(self, data):

        user = self.context['request'].user
        oldpassword = data.get('OldPassword')
        newpassword = data.get('NewPassword')
        confirmpassword = data.get('ConfirmPassword')

        if not user.check_password(oldpassword):
            raise serializers.ValidationError('wrong Password', code='wrong password')
        if newpassword != confirmpassword:
            raise serializers.ValidationError('Not match NewPassword and ConfirmPassword', code='ChangePassword')
        try:
            passvalidate.validate_password(password=newpassword, user=user)
        except ValidationError as error:
            raise serializers.ValidationError(list(error.messages))

        return data
