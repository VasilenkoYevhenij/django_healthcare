from datetime import datetime

import jwt
from django.conf import settings
from rest_framework import authentication, exceptions
from .models import MyUser

ALGORITHM = 'HS256'


class JWTAuthentication(authentication.BaseAuthentication):
    authentication_header_prefix = 'Token'

    def authenticate(self, request):

        request.user = None

        auth_header = authentication.get_authorization_header(request).split()
        auth_header_prefix = self.authentication_header_prefix.lower()

        if not auth_header:
            return None

        if len(auth_header) == 1:

            return None

        elif len(auth_header) > 2:
            return None

        prefix = auth_header[0].decode('utf-8')
        token = auth_header[1].decode('utf-8')

        if prefix.lower() != auth_header_prefix:
            return None
        return self._authenticate_credentials(request, token)

    def _authenticate_credentials(self, request, token):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=ALGORITHM)
        except:
            msg = 'Invalid authentication. Could not decode token.'
            raise exceptions.AuthenticationFailed(msg)

        token_exp = datetime.fromtimestamp(int(payload['exp']))
        if token_exp < datetime.utcnow():
            msg = 'Token expired.'
            raise exceptions.AuthenticationFailed(msg)

        try:
            user = MyUser.objects.get(id=payload['id'])
            return user, token
        except MyUser.DoesNotExist:
            msg = 'No user matching this token was found.'
            raise exceptions.AuthenticationFailed(msg)
