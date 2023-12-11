# redis connection
import redis


REDIS_CLOUD_HOST = 'redis-12770.c274.us-east-1-3.ec2.cloud.redislabs.com'
REDIS_CLOUD_PORT = 12770
REDIS_CLOUD_PASSWORD = 'viO8MRnsgS8D1MeA9cHx6r3s08Tc2qg9'

redis_conn = redis.StrictRedis(
    host=REDIS_CLOUD_HOST,
    port=REDIS_CLOUD_PORT,
    password=REDIS_CLOUD_PASSWORD,
    decode_responses=True,
    )