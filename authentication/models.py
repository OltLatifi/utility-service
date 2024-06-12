import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class User(AbstractUser):
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',
        blank=True,
        verbose_name='groups'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_set',
        blank=True,
        verbose_name='user permissions'
    )

    def __str__(self) -> str:
        return self.email


class Token(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    uuid = models.CharField(default=uuid.uuid4, editable=False, max_length=255)

    def __str__(self) -> str:
        return f"{self.user.email}'s token"
