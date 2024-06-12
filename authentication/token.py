from ninja.security import HttpBearer
from .models import Token


class AuthBearer(HttpBearer):
    def authenticate(self, request, token: str):
        try:
            token: Token = Token.objects.get(uuid=token)
        except:
            return None

        if token:
            return token.uuid
