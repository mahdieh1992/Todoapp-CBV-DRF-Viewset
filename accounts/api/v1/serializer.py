from rest_framework import serializers
from ...models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class AccountSerializers(serializers.ModelSerializer):
    """
        this is serializer model for Rgister user
    """
    password = serializers.CharField(max_length=200, write_only=True, style={'input_type': 'password'})
    ConfirmPassword = serializers.CharField(max_length=200, write_only=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['email', 'password', 'ConfirmPassword']

    def validate(self, attrs):
        """
            evaluate input data according match password and confirmpassword
            evaluate pasword according The password should not be short
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
