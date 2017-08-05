import json


def loads(cls, js):
    ljo = json.loads(js)
    if type(ljo) == list:
        return [load_jo(cls, jo) for jo in ljo]
    else:
        return load_jo(cls, ljo)


def load_jo(cls, jo):
    obj = cls()
    loaders = getattr(cls, 'LOADERS', None)
    if loaders:
        for attr, loader in loaders.items():
            setattr(obj, attr, loader(jo))
    else:
        for attr in jo.keys():
            setattr(obj, attr, jo[attr])
    return obj
