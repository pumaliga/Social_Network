from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from network_app.models import CustomUser, Post
from network_app.tools import is_fan, get_count_like, email_check, clear_data


class SignUpSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password']

    def save(self, **kwargs):
        huntercheck = email_check(self.validated_data["email"])
        if huntercheck == False:
            raise serializers.ValidationError({"email": "Email check is NOT valid."})
        elif len(self.validated_data["password"]) < 8 :
            raise serializers.ValidationError({"password": "password must be at least 8 characters long"})
        self.validated_data["password"] = make_password(self.validated_data["password"])
        return super().save()


class PostSerializer(serializers.ModelSerializer):
    is_fan = serializers.SerializerMethodField()
    author = serializers.SerializerMethodField()
    count_like = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'title', 'text', 'count_like', 'is_fan', 'author']

    def get_is_fan(self, obj):
        """
        checking if the user has licked this post
        """
        user = self.context.get('request').user
        return is_fan(obj, user)

    def get_count_like(self, obj) -> int:
        return get_count_like(obj)

    def get_author(self, obj):
        user = obj.author
        return {'id': user.id, 'username': user.username}

    def validate(self, data):
        data['author_id'] = self.context['request'].user.id
        return data


class FanSerializer(serializers.ModelSerializer):
    user_id = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ['user_id', 'username',]

    def get_user_id(self, obj):
        return obj.id
