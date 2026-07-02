"""
JWT authentication that rejects revoked (blacklisted) tokens — the enforcement half of the
LOCK flow (docs/08, docs/16). Wired via REST_FRAMEWORK DEFAULT_AUTHENTICATION_CLASSES.
"""
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken

from .blacklist import is_blacklisted


class BlacklistAwareJWTAuthentication(JWTAuthentication):
    def get_validated_token(self, raw_token):
        token = super().get_validated_token(raw_token)
        if is_blacklisted(token.get("jti", "")):
            raise InvalidToken("Token has been revoked")
        return token
