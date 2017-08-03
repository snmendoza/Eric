from appevents import Events
from players.baseplayer import BasePlayer


class AudioMsgPlayer(BasePlayer):

    msg_q = []

    def __init__(self):
        super(AudioMsgPlayer, self)
        Events.on_sgh_start_audio_message += self.add_msg
        Events.on_pic_start_audio_message += self.add_msg

    def add_msg(self, command):
        pass
