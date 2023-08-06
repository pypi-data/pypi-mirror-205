from os import path
import pathlib
import shelve
import pickle
from os import environ
from threading import Lock
from flask import current_app

project_root = str(pathlib.Path(__file__).resolve().parents[1])
cache_dir = (path.join(project_root, "cache"))
cache_file = (path.join(cache_dir, "cache"))


class SimpleCache:
    mutex = Lock()

    def __init__(self):
        self.cache_path = environ.get('CACHE_FILE')

    def write_cache(self, dict_name, data):
        self.mutex.acquire()
        shelf = shelve.open(self.cache_path, writeback=True)
        shelf[f"{dict_name}"] = data
        shelf.close()
        self.mutex.release()

    def get_dict(self, dict_name):
        self.mutex.acquire()
        try:
            shelf = shelve.open(self.cache_path)
            data = shelf[f"{dict_name}"]
            shelf.close()
        except KeyError:
            shelf = shelve.open(self.cache_path)
            shelf[dict_name] = {}
            shelf.close()
            return None
        shelf.close()
        self.mutex.release()
        return data

    def get_dict_value(self, dict_name, key_name):
        self.mutex.acquire()
        shelf = shelve.open(self.cache_path)
        try:
            dictionary = shelf[dict_name]
            value = dictionary.get(key_name)
            shelf.close()
            self.mutex.release()
            return value
        except KeyError:
            shelf.close()
            self.mutex.release()
            return None

    def update_dict_value(self, dict_name, data):
        self.mutex.acquire()
        try:
            shelf = shelve.open(self.cache_path, writeback=True)
            dictionary = shelf.get(dict_name)
            dictionary.update(data)
            shelf.close()
            self.mutex.release()
        except AttributeError:
            shelf = shelve.open(self.cache_path, writeback=True)
            shelf[dict_name] = data
            shelf.close()
            self.mutex.release()


class PickleCache:
    masterList = {}
    cache_path = cache_file

    @classmethod
    def update_dict_data(cls, dict_name, data):
        cache = cls.read_all_data().copy()
        if dict_name in cache.keys():
            cache[dict_name].update(data)
        else:
            cache[dict_name] = data
        # if dict_name in current_cache:
        pickle_out = open(cache_file, "wb")
        pickle.dump(cache, pickle_out)
        pickle_out.close()

    @classmethod
    def read_all_data(cls):
        try:
            pickle_in = open(cache_file, "rb")
            data = pickle.load(pickle_in)
            pickle_in.close()
        except FileNotFoundError:
            data = {}
            pickle_out = open(cache_file, "wb")
            pickle.dump(data, pickle_out)
            pickle_out.close()
        return data

    @classmethod
    def get_dict(cls, dict_name):
        data = cls.read_all_data().get(dict_name)
        if data is None:
            cls.update_dict_data(dict_name, {})
            return cls.read_all_data().get(dict_name)
        else:
            return data
