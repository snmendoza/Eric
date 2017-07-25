from flufl.enum import Enum


class AudioMsg(object):

    class Suffix(Enum):
        M = 0
        T = 1
        N = 2

    def __init__(self, command):
        self.key = command.params[1]
        self.room_number = command.params[2]
        self.suffix = self.Suffix[command.params[3]]
