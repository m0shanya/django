from django.db import models
from django.conf import settings


class Profile(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profiles"
    )
    age = models.IntegerField()
    created_at = models.DateTimeField(
        auto_now_add=True, db_index=True
    )
