from appconnections import PICConnection
from appevents import Events
from appm3s import M3S, M3SException
from appvolumemanager import VolumeManager
from collections import deque
from commands import piccommands
from models.audiomsg import AudioMsg
from players.baseplayer import BasePlayer


class AudioMsgPlayer(BasePlayer):

    msg_q = deque([])
    msg = None

    def __init__(self):
        super(AudioMsgPlayer, self)
        Events.on_sgh_start_audio_msg += self.add_msg
        Events.on_pic_start_audio_msg += self.add_msg

    def add_msg(self, command):
        self.msg_q.append(AudioMsg(command))
        if not self.msg:
            Events.on_audio_msg_start()
            self.saved_volume = VolumeManager.volume
            VolumeManager.set_volume(VolumeManager.max)
            self.next()

    def next(self):
        if self.msg_q:
            self.msg = self.msg_q.popleft()
            self.stop()
            try:
                audio_msg = M3S.get_audio_msg_url(self.msg)
                self.set_source(audio_msg.url)
                self.play()
            except M3SException:
                self.on_playback_error()
        else:
            self.msg = None
            VolumeManager.set_volume(self.saved_volume)
            Events.on_audio_msg_end()

    def on_playback_completed(self):
        super(AudioMsgPlayer, self).on_playback_completed()
        self.next()

    def on_playback_error(self):
        super(AudioMsgPlayer, self).on_playback_error()
        self.next()

    def on_play(self, instance):
        super(AudioMsgPlayer, self).on_play(instance)
        PICConnection.send_command(piccommands.SetAudioMsg(True, self.msg.key))

    def on_stop(self, instance):
        PICConnection.send_command(piccommands.SetAudioMsg(False, self.msg.key))
        super(AudioMsgPlayer, self).on_stop(instance)
