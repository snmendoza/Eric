class M3SException(Exception):
    pass


class M3SAPI(object):

    host = None

    def get_music_categories(self):
        return []


M3S = M3SAPI()
