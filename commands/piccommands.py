from basecommands import PICCommand


class Status(PICCommand):
    """This command is sent by the PIC"""
    VALUE = 1


class KeepAlive(PICCommand):

    VALUE = 2

    def __init__(self):
        super(KeepAlive, self).__init__([self.VALUE])


class GetStatus(PICCommand):

    VALUE = 3

    def __init__(self):
        super(GetStatus, self).__init__([self.VALUE])


class SetBright(PICCommand):

    VALUE = 4

    def __init__(self, light_values):
        super(SetBright, self).__init__([self.VALUE] + light_values)


class SetAudio(PICCommand):

    VALUE = 5

    def __init__(self, playing):
        super(SetAudio, self).__init__([self.VALUE, playing])


class SetAudioMessage(PICCommand):

    VALUE = 6

    def __init__(self, playing, msg_key):
        super(SetAudioMessage, self).__init__([self.VALUE, playing, msg_key])


class RecordLightScene(PICCommand):

    VALUE = 7

    def __init__(self, code):
        super(RecordLightScene, self).__init__([self.VALUE, code])


class RecordLightTypes(PICCommand):

    VALUE = 8

    def __init__(self, light_types):
        super(RecordLightTypes, self).__init__([self.VALUE] + light_types)


class ACOn(PICCommand):

    VALUE = 9

    def __init__(self, temp_code):
        super(ACOff, self).__init__([self.VALUE, temp_code])


class ACOff(PICCommand):

    VALUE = 10

    def __init__(self):
        super(ACOff, self).__init__([self.VALUE])


class SetACTemp(PICCommand):

    VALUE = 11

    def __init__(self, temp_code):
        super(SetACTemp, self).__init([self.VALUE, temp_code])


class Intro(PICCommand):
    """This command is sent by the PIC"""
    VALUE = 12


class VideoOnOff(PICCommand):

    VALUE = 13

    def __init__(self):
        super(VideoOnOff, self).__init__([self.VALUE])


class ChannelUp(PICCommand):

    VALUE = 14

    def __init__(self):
        super(ChannelUp, self).__init__([self.VALUE])


class ChannelDown(PICCommand):

    VALUE = 15

    def __init__(self):
        super(ChannelDown, self).__init__([self.VALUE])


class VolumeUp(PICCommand):

    VALUE = 16

    def __init__(self):
        super(VolumeUp, self).__init__([self.VALUE])


class VolumeDown(PICCommand):

    VALUE = 17

    def __init__(self):
        super(VolumeDown, self).__init__([self.VALUE])


class Macro(PICCommand):

    VALUE = 18

    def __init__(self, number):
        numbers = [number / 100, (number % 100) / 10, number % 10]
        super(Macro, self).__init__([self.VALUE] + numbers)


class Info(PICCommand):

    VALUE = 19

    def __init__(self):
        super(Info, self).__init__([self.VALUE])


class Digit(PICCommand):

    BASE_VALUE = 20

    def __init__(self, digit):
        super(Digit, self).__init__([self.BASE_VALUE + digit])


class SetTVRemoteCode(PICCommand):

    VALUE = 30

    def __init__(self, remote_code):
        super(SetTVRemoteCode, self).__init__([self.VALUE, remote_code])


class VideoSource(PICCommand):

    VALUE = 31

    def __init__(self):
        super(VideoSource, self).__init__([self.VALUE])


class VideoMute(PICCommand):

    VALUE = 32

    def __init__(self):
        super(VideoMute, self).__init__([self.VALUE])
