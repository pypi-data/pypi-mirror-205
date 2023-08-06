import redis


class CuckooFilterRedis:
    def __init__(self,
                 redis_url: str,
                 key: str = "cuckoofilter",
                 bucket_size: int = 1,
                 expansion: int = 1,
                 capacity: int = 27
                 ):
        """
        redis_url: redis url
        key: redis key
        bucket_size: 桶的大小,桶越大错误率越高, 但过滤器填充率越高 等于1时错误率最小为0.78%，等于3时为2.35%,
        expansion: 支持扩展容量的次数, 扩展次数越多，错误率越高
        capacity: 容量 去重数量 2 ** 27 = 134,217,728
        """
        self.server = redis.StrictRedis.from_url(redis_url, decode_responses=True)
        self.key = key
        self.bucket_size = bucket_size
        self.expansion = expansion
        self.capacity = capacity
        self.cf = self.server.cf()
        self.valid_redis_has_bloom()
        if not self.server.exists(key):
            self.cf.create(key, capacity, expansion=expansion, bucket_size=bucket_size)
        else:
            if self.server.type(key) != "MBbloomCF":
                self.server.delete(key)
                self.cf.create(key, capacity, expansion=expansion, bucket_size=bucket_size)

    def valid_redis_has_bloom(self):
        try:
            self.cf.info('a')
        except Exception as e:
            if "unknown command" in str(e):
                raise Exception("redis not support cuckoo filter, please install redisbloom module")

    def add(self, value):
        return self.cf.addnx(self.key, value)

    def exists(self, value):
        return self.cf.exists(self.key, value)

    def delete(self, value):
        return self.cf.delete(self.key, value)

    def info(self):
        return self.cf.info(self.key)
