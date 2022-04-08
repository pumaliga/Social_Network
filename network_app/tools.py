from django.contrib.contenttypes.models import ContentType

from .models import Like
from django.contrib.auth import get_user_model
import requests


User = get_user_model()

EMAILHUNTER = 'your api key'


def add_like(obj, user):
    obj_type = ContentType.objects.get_for_model(obj)
    like, is_created = Like.objects.get_or_create(content_type=obj_type, object_id=obj.id, user=user)
    return like


def remove_like(obj, user):
    obj_type = ContentType.objects.get_for_model(obj)
    Like.objects.filter(content_type=obj_type, object_id=obj.id, user=user).delete()


def is_fan(obj, user) -> bool:
    obj_type = ContentType.objects.get_for_model(obj)
    likes = Like.objects.filter(content_type=obj_type, object_id=obj.id, user=user)

    return likes.exists()


def get_fans(obj):
    obj_type = ContentType.objects.get_for_model(obj)
    return User.objects.filter(likes__content_type=obj_type, likes__object_id=obj.id)


def get_count_like(obj):
    obj_type = ContentType.objects.get_for_model(obj)
    return Like.objects.filter(content_type=obj_type, object_id=obj.id).count()


def get_total_likes_or_data_range(date_from, date_to):
    count_of_likes = Like.objects.filter(create_at__gte=date_from, create_at__lte=date_to).count()
    return count_of_likes


def email_check(email):
    key = EMAILHUNTER
    req = {"api_key":key, "email":email}
    odg = requests.get("https://api.hunter.io/v2/email-verifier", params=req)
    data = odg.json()
    data = data["data"]
    if data["gibberish"] == False and data["webmail"] == True:
        return True
    else:
        return False

