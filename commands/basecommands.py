class BaseCommand(object):

    START = bytearray([0x29])
    END = bytearray([0, 0])

    def __init__(self, node_len, params):
        node = params[:node_len] + [0] * (node_len - len(params))
        self.values = self.START + bytearray(node) + self.END


class PICCommand(BaseCommand):

    NODE_LEN = 12

    def __init__(self, params):
        super(PICCommand, self).__init__(self.NODE_LEN, params)


class SGHCommand(BaseCommand):

    NODE_LEN = 200

    def __init__(self, params):
        super(SGHCommand, self).__init__(self.NODE_LEN, params)
