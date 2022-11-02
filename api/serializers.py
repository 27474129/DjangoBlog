from core.models import Article
from users.models import User
from .models import Mark, Comment
from rest_framework import serializers
from users.validators import UserValidators


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class UserPkSerializer(serializers.Serializer):
    pk = serializers.IntegerField()
