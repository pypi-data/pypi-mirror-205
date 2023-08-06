import json


class dict(dict):
    def nget(self, key, default=None):
        # nested get
        if '/' in key:
            k1, k2 = key.split('/', 1)
            try:
                k1 = int(k1)
            except ValueError:
                pass
            return dict(self[k1]).nget(k2, default) if k1 in self else None
        else:
            return json.dumps(self[key]) if isinstance(self.get(key), (dict, list)) else self.get(key, default)

    def gets(self, keys, default=None):
        # nested gets
        if default is None:
            default = {}
        return [self.nget(k, default.get(k)) for k in keys]

    # @property
    # def __class__(self):
    #     return super().__class__()
