import time

from rest_framework import serializers
from Todo.models import Todo
import json
from time import sleep
import requests

class TodoSerializer(serializers.ModelSerializer):
    """
    create ModelSerializer todo
    """

    class Meta:
        model = Todo
        fields = ["id", "Title", "Is_active", "Completed", "CreateDate"]

    def to_representation(self, instance):
        """
        override createdate in TodoDetail
        """
        request = self.context.get("request")
        rep = super().to_representation(instance)
        if request.parser_context.get("kwargs").get("pk"):
            rep.pop("CreateDate", None)
        return rep


class CitySerializer(serializers.Serializer):
    cityname = serializers.CharField(max_length=30)

    def validate(self, data):
        request = self.context.get('request')
        city=data.get('cityname')
        api_key = 'f5e41cf196b2c9120d695625b12abf5e'
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'

        response = requests.get(url)
        data['city_weather'] = response.json()
        return data