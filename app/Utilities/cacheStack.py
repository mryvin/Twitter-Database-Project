import pickle

class LRUCache:
    def __init__(self):
        self.capacity = 5
        self.cache = {}
        self.counter = 0

    def get(self, key):
        if key not in self.cache:
            return -1
        else:
            self.counter += 1
            self.cache[key]['counter'] = self.counter
            return self.cache[key]['value']

    def put(self, key, value):
        if key in self.cache:
            self.cache[key]['value'] = value
            self.counter += 1
            self.cache[key]['counter'] = self.counter
        else:
            if len(self.cache) >= self.capacity:
                lru_key = min(self.cache, key=lambda k: self.cache[k]['counter'])
                self.cache.pop(lru_key)
            self.cache[key] = {'value': value, 'counter': 0}
        if self.counter % 5 == 0:
            with open('cache.pickle', 'wb') as f:
                pickle.dump(self.cache, f)
