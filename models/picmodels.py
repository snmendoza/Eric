from commands.basecommands import PICCommand


class Info(object):

    def __init__(self, command):
        offset = len(PICCommand.START)
        self.light_values = command[offset:offset + 6]
        self.ac_status = command[offset + 6]
        self.ac_temp_code = command[offset + 7]
