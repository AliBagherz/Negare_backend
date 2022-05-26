from django.db import models
from authentication.models import AppUser
from core.models import BaseModel
from django.utils.translation import gettext_lazy as _


class MessageTypeChoices(models.TextChoices):
    MUSIC = 'M', _('music')
    VIDEO = 'V', _('video')
    PICTURE = 'P', _('picture')
    TEXT = 'T', _('text')


class Chat(BaseModel):
    chat_code = models.CharField(max_length=200, unique=True)
    users = models.ManyToManyField(AppUser, related_name='chats')


class Message(BaseModel):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    sender_index = models.IntegerField(default=0)
    type = models.CharField(
        max_length=1,
        choices=MessageTypeChoices.choices,
        default=MessageTypeChoices.TEXT
    )
    text = models.CharField(max_length=2000, null=True, blank=True)
    image = models.ForeignKey(
        "core.Image",
        on_delete=models.CASCADE,
        related_name='message',
        null=True,
        blank=True
    )
    content = models.ForeignKey("core.Content", on_delete=models.CASCADE, related_name='message', null=True, blank=True)

    def __str__(self):
        if self.type == MessageTypeChoices.TEXT:
            return self.text
        return self.get_type_display()
