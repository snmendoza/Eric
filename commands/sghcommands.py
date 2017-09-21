from basecommands import SGHCommand


class Status(SGHCommand):
    """This command is sent by the SGH"""
    VALUE = 1


class EricStatus(SGHCommand):

    VALUE = 2

    def __init__(self, plugged, rebooting):
        super(EricStatus, self).__init__([self.VALUE, plugged, rebooting])


class KeepAlive(SGHCommand):
    """This command is sent by the SGH"""
    VALUE = 3


class StartAudioMsg(SGHCommand):
    """This command is sent by the SGH"""
    VALUE = 4


class GetAccountInfo(SGHCommand):

    VALUE = 5

    def __init__(self):
        super(GetAccountInfo, self).__init__([self.VALUE])


class AccountInfo(SGHCommand):
    """This command is sent by the SGH"""
    VALUE = 6
