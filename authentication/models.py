import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UsagePermission(BaseModel):
    name = models.CharField(max_length=255)
    requests_per_second = models.PositiveIntegerField()

    def __str__(self) -> str:
        return f"{self.name} - {self.requests_per_second} "


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
    usage_permission = models.ManyToManyField(
        UsagePermission,
        related_name='user',
        blank=True,
        verbose_name='Usage permissions'
    )

    def __str__(self) -> str:
        return self.email


class Token(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    uuid = models.CharField(default=uuid.uuid4, editable=False, max_length=255)

    def __str__(self) -> str:
        return f"{self.user.email}'s token"


class Request(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.ForeignKey(Token, on_delete=models.CASCADE)
    endpoint = models.CharField(max_length=255, editable=False)

    def __str__(self) -> str:
        return f"{self.endpoint} - {self.user}"
