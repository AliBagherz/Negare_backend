from datetime import timedelta
import random

import redis
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


def get_otp_code(user_id: int) -> str:
    otp_code = str(random.randint(1000, 9999))
    broker = redis.Redis("redis", 6379)
    broker.set('otp_' + str(user_id), otp_code, timedelta(minutes=2))
    return otp_code


def is_otp_code_valid(user_id: int, otp_code: str) -> bool:
    broker = redis.Redis("redis", 6379)
    saved_otp_byte = broker.get('otp_' + str(user_id))
    if not saved_otp_byte:
        return False
    saved_otp = saved_otp_byte.decode('UTF-8')
    return saved_otp == otp_code
