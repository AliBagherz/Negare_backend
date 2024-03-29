from django.db import models
from core.models import BaseModel, Image


class Category(BaseModel):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name
