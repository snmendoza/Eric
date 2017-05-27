class BaseCommand(object):

    START = bytearray([0x29])
    END = bytearray([0, 0])

    def __init__(self, node_length, params):
        self.values = self.START + params[:node_length] + self.END
