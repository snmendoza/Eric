import jsonloader
from kivy.logger import Logger
from models import m3smodels
import requests


class M3SException(Exception):
    pass


class M3SAPI(object):

    host = None

    def get_music_categories(self):
        return jsonloader.loads(
            m3smodels.MusicCategory, self.make_request('api/get-radios'))

    def get_songs(self, category):
        return jsonloader.loads(
            m3smodels.Song,
            self.make_request('api/get-radio-songs', id=category.id))

    def get_audio_msg_url(self, msg):
        return jsonloader.loads(m3smodels.AudioMessage,
                                self.make_request(
                                    'api/get-audio-message',
                                    key=msg.key,
                                    room=msg.room_number,
                                    suffix=msg.suffix))

    def make_request(self, endpoint, **kwargs):
        url = 'http://' + self.host + '/' + endpoint
        try:
            r = requests.get(url, params=kwargs)
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
