import jsonloader
from kivy.logger import Logger
from models.musiccategory import MusicCategory
import requests


class M3SException(Exception):
    pass


class M3SAPI(object):

    host = None

    def get_music_categories(self):
        return jsonloader.loads(
            MusicCategory, self.make_request('api/get-radios'))

    def get_songs(self, category):
        return []

    def make_request(self, endpoint, **kwargs):
        url = 'http://' + self.host + '/' + endpoint
        try:
            r = requests.get(url)
        except Exception as e:
            Logger.warning(__name__ + ': ' + str(e))
            raise M3SException(str(e))
        if r.status_code != 200:
            error_msg = 'Error getting response (' + str(r.status_code) + \
                ') from ' + url
            Logger.warning(__name__ + ': ' + error_msg)
            raise M3SException(error_msg)
        else:
            return r.text


M3S = M3SAPI()
