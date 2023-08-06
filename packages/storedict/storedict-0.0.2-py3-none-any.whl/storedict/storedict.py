from collections.abc import MutableMapping

import requests


class ProxyError(Exception):
    pass


class BaseStore(MutableMapping):
    """Keys must be strings"""

    def __getitem__(self, key):
        ...

    def __setitem__(self, key, value):
        ...

    def __delitem__(self, key):
        ...

    def __iter__(self):
        ...

    def __len__(self):
        ...

    def __contains__(self, key):
        ...

    def get(self, key, default=None):
        ...

    def items(self):
        ...

    def keys(self):
        ...

    def values(self):
        ...

    def clear(self):
        ...

    def validate_key(self, key):
        if not isinstance(key, str):
            raise TypeError("Key must be a string")

    def validate_value(self, value):
        """
        Values must be strings, ints, dicts, or lists. Nested objects should
        follow the same rule. All dict keys must be strings.
        """
        if isinstance(value, (str, int, bool)):
            return
        elif isinstance(value, dict):
            for k, v in value.items():
                if not isinstance(k, str):
                    raise TypeError("Dictionary keys must be strings")
                self.validate_value(v)
        elif isinstance(value, list):
            for item in value:
                self.validate_value(item)
        else:
            raise TypeError("Value must be a string, int, bool, dict, or list")


class LocalStore(BaseStore):
    def __init__(self):
        super().__init__()
        self._store = {}

    def __getitem__(self, key):
        self.validate_key(key)
        return self._store[key]

    def __setitem__(self, key, value):
        self.validate_key(key)
        self.validate_value(value)
        self._store[key] = value

    def __delitem__(self, key):
        self.validate_key(key)
        del self._store[key]

    def __iter__(self):
        return iter(self._store)

    def __len__(self):
        return len(self._store)

    def __contains__(self, key):
        self.validate_key(key)
        return key in self._store

    def get(self, key, default=None):
        self.validate_key(key)
        return self._store.get(key, default)

    def items(self):
        return self._store.items()

    def keys(self):
        return self._store.keys()

    def values(self):
        return self._store.values()

    def clear(self):
        self._store.clear()


class ProductionStore(BaseStore):
    def __init__(self, datastore_proxy_url):
        super().__init__()
        self.datastore_proxy_url = datastore_proxy_url
        self.urls = {
            "key-exists": self.datastore_proxy_url + "/key-exists",
            "put-value": self.datastore_proxy_url + "/put-value",
            "get-value": self.datastore_proxy_url + "/get-value",
            "get-items": self.datastore_proxy_url + "/get-items",
            "delete-item": self.datastore_proxy_url + "/delete-item",
            "count": self.datastore_proxy_url + "/count",
            "clear": self.datastore_proxy_url + "/clear",
        }

    def __getitem__(self, key):
        self.validate_key(key)
        r = requests.post(self.urls["get-value"], json={"key": key})
        if r.status_code == 404:
            raise KeyError()
        if r.status_code != 200:
            raise ProxyError()
        return r.json()

    def __setitem__(self, key, value):
        self.validate_key(key)
        self.validate_value(value)
        r = requests.post(self.urls["put-value"], json={"key": key, "value": value})
        if r.status_code != 200:
            raise ProxyError()

    def __delitem__(self, key):
        self.validate_key(key)
        r = requests.post(self.urls["delete-item"], json={"key": key})
        if r.status_code == 404:
            raise KeyError()
        if r.status_code != 200:
            raise ProxyError()

    def __iter__(self):
        r = requests.post(self.urls["get-items"])
        if r.status_code != 200:
            raise ProxyError()
        return iter(r.json())

    def __len__(self):
        r = requests.post(self.urls["count"])
        if r.status_code != 200:
            raise ProxyError()
        return r.json()

    def __contains__(self, key):
        self.validate_key(key)
        r = requests.post(self.urls["key-exists"], json={"key": key})
        if r.status_code == 404:
            return False
        if r.status_code == 200:
            return True
        raise ProxyError()

    def get(self, key, default=None):
        self.validate_key(key)
        r = requests.post(self.urls["get-value"], json={"key": key})
        if r.status_code == 404:
            return default
        if r.status_code != 200:
            raise ProxyError()
        return r.json()

    def items(self):
        r = requests.post(self.urls["get-items"])
        if r.status_code != 200:
            raise ProxyError()
        return r.json().items()

    def keys(self):
        r = requests.post(self.urls["get-items"])
        if r.status_code != 200:
            raise ProxyError()
        return r.json().keys()

    def values(self):
        r = requests.post(self.urls["get-items"])
        if r.status_code != 200:
            raise ProxyError()
        return r.json().values()

    def clear(self):
        r = requests.post(self.urls["clear"])
        if r.status_code != 200:
            raise ProxyError()


def create_store(datastore_proxy_url=None):
    if datastore_proxy_url is None:
        return LocalStore()
    else:
        return ProductionStore(datastore_proxy_url)
