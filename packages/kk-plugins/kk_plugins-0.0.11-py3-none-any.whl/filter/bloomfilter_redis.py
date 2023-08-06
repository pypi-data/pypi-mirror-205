import redis


class BloomfilterRedis:
    def __init__(self,
                 redis_url: str,
                 key: str = "bloomfilter",
                 error_rate: float = 0.0001,
                 capacity: int = 10000000,
                 ):
        """
        redis_url: redis url
        key: redis key
        errorRate: 去重错误率
        capacity: 去重数量
        """
        self.server = redis.StrictRedis.from_url(redis_url, decode_responses=True)
        self.key = key
        self.errorRate = error_rate
        self.capacity = capacity
        self.bf = self.server.bf()
        self.valid_redis_has_bloom()
        if not self.server.exists(key):
            self.bf.create(key, error_rate, capacity)
        else:
            if self.server.type(key) != "MBbloom--":
                self.server.delete(key)
                self.bf.create(key, error_rate, capacity)

    def valid_redis_has_bloom(self):
        try:
            self.bf.info('a')
        except Exception as e:
            if "unknown command" in str(e):
                raise Exception("redis not support bloom filter, please install redisbloom module")

    def add(self, value):
        return self.bf.add(self.key, value)

    def exists(self, value):
        return self.bf.exists(self.key, value)
