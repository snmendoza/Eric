import urllib


class MusicCategory(object):
    pass


class Song(object):

    LOADERS = {
        'title': lambda jo: jo['title'],
        'album': lambda jo: jo['album'],
        'artist': lambda jo: jo['author'],
        'url': lambda jo: urllib.quote(jo['songUrl'], safe=':/'),
        'albumart_url': lambda jo: urllib.quote(jo['albumartUrl'], safe=':/'),
    }


class AudioMessage(object):

    LOADERS = {
        'url': lambda jo: jo['audioMessageUrl']
    }
