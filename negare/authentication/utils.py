from rest_framework.response import Response

from .models import AppUser


def register_user(data):
    user = AppUser(**data)
    user.set_password(data['password'])
    try:
        user.save()
    except Exception as e:
        a = e.args
        return Response({"error": e.args[0]})
    return user
