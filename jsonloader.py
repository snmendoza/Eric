import json


def loads(cls, js):
    ljo = json.loads(js)
    if type(ljo) == list:
        return [load_jo(cls, jo) for jo in ljo]
    else:
        return load_jo(cls, ljo)


def load_jo(cls, jo):
    obj = cls()
    loaders = cls.LOADERS if hasattr(cls, 'LOADERS') else get_def_loaders(jo)
    for attr, loader in loaders.items():
        setattr(obj, attr, loader(jo))
    return obj


def get_def_loaders(jo):
    return {attr: (lambda jo: val) for attr, val in jo.items()}
