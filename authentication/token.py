from imagecompressor.exceptions import ThrottleError
from ninja.security import HttpBearer

from .models import Token, User, Request

from datetime import datetime
from django.utils.timezone import make_aware, get_current_timezone


class AuthBearer(HttpBearer):
    requestPerSec = 1

    def authenticate(self, request, token: str):
        endpoint_url: str = request.get_full_path()

        try:
            token: Token = Token.objects.get(uuid=token)
            user: User = token.user
        except:
            return None

        if not self.requestThrottle(user):
            raise ThrottleError

        Request.objects.create(
            user=user,
            token=token,
            endpoint=endpoint_url
        )

        if token:
            return token.uuid

    def requestThrottle(self, user: User) -> bool:
        current_time: datetime = make_aware(
            datetime.now(), get_current_timezone())

        last_request: Request = Request.objects.filter(
            user=user,
        ).last()

        if last_request:
            request_time: datetime = last_request.created_at
            print("here ->", (current_time - request_time).total_seconds())

            return (current_time - request_time).total_seconds() > self.requestPerSec
        return True
