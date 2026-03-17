import time
from typing import Any
from functools import lru_cache
import random

class cached_object():
    def __init__(self, id:Any, value:Any, after:Any|None, before:Any|None):
        try:
            self.id = hash(id)
        except Exception as e:
            raise Exception(f'provided id is not hashable with message f{str(e)}')
        self.value = value
        self.before = before
        self.after = after
        self.last_access_time: float | None = None
        self.access_count:int = 0

    def __repr__(self):
        return f'cached object id = {self.id} , value = {self.value}'


class cache():
    def __init__(self, cache_type:str, cache_size=5):
        self.cache_type = cache_type
        self.cache_size = cache_size
        self.object_count: int = 0
        self.object_ids : list|None = None
        self.head : cached_object|None = None
    
    def __repr__(self):
        text = ''
        node = self.head
        while node:
            text+=f'{node.id},'
            node = node.after
        return text[:-1]
    def move_to_head(self, node: cached_object):
        if node is self.head:
            return
        if node.before:
            node.before.after = node.after
        if node.after:
            node.after.before = node.before
        node.before = None
        node.after = self.head
        if self.head:
            self.head.before = node
        self.head = node

    def insert(self, id, value):
        # print (f'inserting {id} with value {value} in cache')
        if self.head is not None:
            self.move_to_head(cached_object(id=id, value=value, after = None, before=None))
            if self.object_count < self.cache_size:
                self.object_count += 1
            else: # handle the case when number of cached node is the max allowed
                node = self.head
                while node.after:
                    node = node.after
                # print (f'The last node is {node}')
                node.before.after = None
                del node
        else:
            self.head = cached_object(id=id, value=value, after = None, before=None)
            self.object_count += 1
        # print (f'node {self.head} is inserted')

    def readFromCashSequentially(self, id):
        node = self.head
        hashed_id = hash(id)
        while node:
            if node.id == hashed_id:
                # print(f'found {node.value} in cache')
                self.move_to_head(node)
                return node.value
            node = node.after
        return None

def cache_this(cache_size):
    print(f'cache size in decorator is {cache_size}')
    this_cache = cache('LRU', cache_size=cache_size)
    def decoratror(func):
        def wrapper(*args,**kwargs):
            keys = args , tuple(kwargs.items())
            result_in_cache = this_cache.readFromCashSequentially(keys)
            if result_in_cache is not None: 
                return result_in_cache
            else:
                result = func(*args, **kwargs)
                this_cache.insert(keys, result)
                return result
        return wrapper 
    return decoratror

def test():
    print("Hello from lru-cache!")
    cache_size = 30
    sleep_time = 0.001
    nums = random.choices(range(1, 300), k=5000)
    print(f'Length of nums is {len(nums)}')
    
    @cache_this(cache_size)
    def test_func_myCache(x):
        time.sleep(sleep_time) # to make the function more time consuming and see the effect of caching
        return x*x

    @lru_cache(maxsize=cache_size)
    def test_func_pyLRU(x):
        time.sleep(sleep_time) # to make the function more time consuming and see the effect of caching
        return x*x

    def test_func_no_cache(x):
        time.sleep(sleep_time) # to make the function more time consuming and see the effect of caching
        return x*x

    print('testing my cache')
    start = time.time()
    for num in nums:
        test_func_myCache(num)
    
    mycache_duration = time.time() - start

    print(f'testing my cache took {mycache_duration} seconds')
    print('testing python lru cache')
    start = time.time()
    for num in nums:
        test_func_pyLRU(num)
    pylru_duration = time.time() - start
    print(f'testing python lru cache took {pylru_duration} seconds')
    print(f'pyLRU is {mycache_duration/pylru_duration} times faster than my cache')

    start = time.time()
    for num in nums:
        test_func_no_cache(num)
    no_cache_duration = time.time() - start
    print(f'testing no cache took {no_cache_duration} seconds')
    print(f'no cache is {mycache_duration/no_cache_duration} times faster than my cache')


if __name__ == "__main__":
    test()
