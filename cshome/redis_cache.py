import redis

from cshome.settings import REDIS_HOST, REDIS_PORT

r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)


def push_url(key, url):
    r.rpush(key, url)