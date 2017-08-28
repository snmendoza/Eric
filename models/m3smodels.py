class MusicCategory(object):
    pass


class Song(object):

    LOADERS = {
        'title': lambda jo: jo['title'],
        'album': lambda jo: jo['album'],
        'artist': lambda jo: jo['author'],
        'url': lambda jo: jo['songUrl'],
        'albumart_url': lambda jo: jo['albumartUrl']
    }


class AudioMessage(object):

    LOADERS = {
        'url': lambda jo: jo['audioMessageUrl']
    }
