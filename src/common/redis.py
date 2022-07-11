from django.conf import settings

from redis import ConnectionPool, Redis


pool: ConnectionPool = ConnectionPool.from_url(
    settings.REDIS['URL'], password=settings.REDIS['PASSWORD'], port=settings.REDIS['PORT'],
    decode_responses=True, max_connections=10)
redis_client: Redis = Redis(connection_pool=pool, decode_responses=True)
