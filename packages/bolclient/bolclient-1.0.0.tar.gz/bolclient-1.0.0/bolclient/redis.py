import redis


class Redis:

    def __init__(self, hostname, password=None, port=None, database=None, connection_method=None):
        """
        :param hostname: localhost
        :param password:
        :param port: 6379
        :param database: 0
        :param connection_method: redis://
        """
        self.hostname = hostname
        self.password = password
        self.port = port or 6379
        self.database = database or 0
        self.connection_method = connection_method or "redis://"

    @property
    def redis_client(self):
        """
        :return: redis connection client
        """
        return redis.StrictRedis(
            host=self.hostname,
            port=self.port,
            db=self.database,
            password=self.password,
            charset="utf-8",
            decode_responses=True
        )
