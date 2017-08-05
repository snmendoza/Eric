class MusicCategory(object):
    pass


class Song(object):

    LOADER = {
        'title': lambda jo: jo['title'],
        'album': lambda jo: jo['album'],
        'artist': lambda jo: jo['artist'],
        'url': lambda jo: jo['songUrl'],
        'albumart_url': lambda jo: jo['albumartUrl'],
    }
