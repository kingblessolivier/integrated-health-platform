"""JWT blacklist (docs/08, docs/16 LOCK). Backed by the cache (Redis in prod)."""
from django.core.cache import cache

_PREFIX = "jwt_blacklist:"


def blacklist_jti(jti: str, ttl: int = 28800) -> None:
    cache.set(f"{_PREFIX}{jti}", True, ttl)


def is_blacklisted(jti: str) -> bool:
    return bool(cache.get(f"{_PREFIX}{jti}"))
