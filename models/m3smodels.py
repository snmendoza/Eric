import urllib


def quote_url(jo, attr):
    return urllib.quote(jo[attr], safe=':/') if jo[attr] else None


class MusicCategory(object):
    pass


class Song(object):

    LOADERS = {
        'title': lambda jo: jo['title'],
        'album': lambda jo: jo['album'],
        'artist': lambda jo: jo['author'],
        'url': lambda jo: quote_url(jo, 'songUrl'),
        'albumart_url': lambda jo: quote_url(jo, 'albumartUrl')
    }


class AudioMessage(object):

    LOADERS = {
        'url': lambda jo: quote_url(jo, 'audioMessageUrl'),
    }
