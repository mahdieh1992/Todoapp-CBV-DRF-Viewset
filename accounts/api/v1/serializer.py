from rest_framework import serializers
from ...models import User
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import authenticate


class LoginUserSerializers(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    password = serializers.CharField(label=_('password'), max_length=255, style={'input_type': 'password'},
                                     write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        if email and password:
            user = authenticate(request=self.context.get('request'), email=email, password=password)
            if not user:
                raise serializers.ValidationError('user is not exists', code=1)
        else:
            raise serializers.ValidationError('must include email and password', code=2)
        data['user'] = user
        return data


class RegisterSerializer(serializers.ModelSerializer):
    confirmPassword = serializers.CharField(max_length=255,style={'input_type':'password'})
    password = serializers.CharField(max_length=255,style={'input_type':'password'})

    class Meta:
        model = User
        fields = ['email', 'password', 'confirmPassword']

    def validate(self, data):
        password = data.get('password')
        confirmPassword = data.get('confirmPassword')
        email=data.get('email')
        if password != confirmPassword:
            raise serializers.ValidationError('Not match password and Confirm password')
        if User.objects.filter(email=email,password=password).exists():
            raise serializers.ValidationError('User is exists')
        return data
