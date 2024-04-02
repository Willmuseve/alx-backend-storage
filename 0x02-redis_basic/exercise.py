#!/usr/bin/env python3
"""Import modules for Redis torage"""

import uuid
import redis
from functools import wraps
from typing import Any, Callable, Union


def count_calls(method: Callable) -> Callable:
    """
    Function that counts how many times methods of Cache class are called.
    """
    @wraps(method)
    def invoker(self, *args, **kwargs) -> Any:
        """
        function invoker
        """
        if isinstance(self._redis, redis.Redis):
            self._redis.incr(method.__qualname__)
        return (method(self, *args, **kwargs))
    return (invoker)


def call_history(method: Callable) -> Callable:
    """
    gunc call history
    """
    @wraps(method)
    def invoker(self, *args, **kwargs) -> Any:
        """
        Returns method output after storing its
        inputs and output.
        """
        input_key = '{}:inputs'.format(method.__qualname__)
        output_key = '{}:outputs'.format(method.__qualname__)

        if isinstance(self._redis, redis.Redis):
            self._redis.rpush(input_key, str(args))

        output = method(self, *args, **kwargs)

        if isinstance(self._redis, redis.Redis):
            self._redis.rpush(output_key, output)
        return (output)
    return (invoker)


def replay(fn: Callable) -> None:
    """Displays the history of calls of a particular function"""
    if fn is None or not hasattr(fn, '__self__'):
        return
    redis_store = getattr(fn.__self__, '_redis', None)
    if not isinstance(redis_store, redis.Redis):
        return
    fxn_name = fn.__qualname__
    input_key = '{}:inputs'.format(fxn_name)
    output_key = '{}:outputs'.format(fxn_name)
    fxn_call_count = 0

    if redis_store.exists(fxn_name) != 0:
        fxn_call_count = int(redis_store.get(fxn_name))
    print('{} was called {} times:'.format(fxn_name, fxn_call_count))

    fxn_inputs = redis_store.lrange(input_key, 0, -1)
    fxn_outputs = redis_store.lrange(output_key, 0, -1)

    for fxn_input, fxn_output in zip(fxn_inputs, fxn_outputs):
        print('{}(*{}) -> {}'.format(
              fxn_name,
              fxn_input.decode('utf-8'),
              fxn_output,
              ))


class Cache:
    """
    Class represents object for Redis data storage
    """
    def __init__(self) -> None:
        """Initialises class instance"""
        self._redis = redis.Redis()
        self._redis.flushdb(True)

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Stores a value in Redis data storage and returns a key"""
        data_key = str(uuid.uuid4())
        self._redis.set(data_key, data)
        return (data_key)

    def get(
            self,
            key: str,
            fn: Callable = None,
            ) -> Union[str, bytes, int, float]:
        """Gets value from Redis data storage"""
        data = self._redis.get(key)
        return fn(data) if fn is not None else data

    def get_str(self, key: str) -> str:
        """Gets string value from Redis data storage"""
        return self.get(key, lambda x: x.decode('utf-8'))

    def get_int(self, key: str) -> int:
        """Gets an integer value from Redis data storage"""
        return self.get(key, lambda x: int(x))
