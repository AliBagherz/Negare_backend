from django.core.mail import send_mail
from authentication.models import AppUser
from authentication.utils import get_otp_code
from negare.celery import app
from negare.settings import EMAIL_HOST_USER


@app.task(bind=True)
def send_email(self, *args):
    user = AppUser.objects.get(pk=args[0])
    otp_code = get_otp_code(args[0])
    send_mail(
        'OTP Code - Negare',
        f'Hi {user.first_name}!\nYour otp_code is: {otp_code}',
        EMAIL_HOST_USER,
        [user.email]
    )
