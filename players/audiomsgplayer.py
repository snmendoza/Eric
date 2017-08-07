from appconnections import PICConnection
from appevents import Events
from appm3s import M3S, M3SException
from collections import deque
from commands import piccommands
from models.audiomsg import AudioMsg
from players.baseplayer import BasePlayer


class AudioMsgPlayer(BasePlayer):

    msg_q = deque([])
    msg = None

    def __init__(self):
        super(AudioMsgPlayer, self)
        Events.on_sgh_start_audio_message += self.add_msg
        Events.on_pic_start_audio_message += self.add_msg

    def add_msg(self, command):
        Events.on_audio_msg_start()
        self.msg_q.append(AudioMsg(command))
        if not self.msg:
            self.next()

    def next(self):
        if self.msg_q:
            self.msg = self.msg_q.popleft()
            try:
                url = M3S.get_audio_msg_url(self.msg)
                self.set_source(url)
                self.play()
            except M3SException:
                self.on_playback_error()
        else:
            self.msg = None
            Events.on_audio_msg_end()

    def on_playback_completed(self):
        super(AudioMsg, self).on_playback_completed(self)
        self.next()

    def on_playback_error(self):
        super(AudioMsg, self).on_playback_error(self)
        self.next()

    def on_play(self):
        super(AudioMsg, self).on_play()
        PICConnection.send_command(piccommands.SetAudioMsg(True, self.msg.key))

    def on_stop(self):
        super(AudioMsg, self).on_stop()
        PICConnection.send_command(piccommands.SetAudioMsg(False, self.msg.key))
