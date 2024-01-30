from rest_framework import serializers
from Todo.models import Todo


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
