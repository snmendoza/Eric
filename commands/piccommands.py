from basecommands import PICCommand


class KeepAlive(PICCommand):

    VALUE = 2

    def __init__(self):
        super(KeepAlive, self).__init__([self.VALUE])


class GetStatus(PICCommand):

    VALUE = 3

    def __init__(self):
        super(GetStatus, self).__init__([self.VALUE])


class RecordLightScene(PICCommand):

    VALUE = 7

    def __init__(self, code):
        super(RecordLightScene, self).__init__([self.VALUE, code])


class ACOn(PICCommand):

    VALUE = 9

    def __init__(self, temp_code):
        super(ACOff, self).__init__([self.VALUE, temp_code])


class ACOff(PICCommand):

    VALUE = 10

    def __init__(self):
        super(ACOff, self).__init__([self.VALUE])


class Intro(PICCommand):

    VALUE = 12

    def __init__(self):
        super(Intro, self).__init__([self.VALUE])


class ChannelUp(PICCommand):

    VALUE = 14

    def __init__(self):
        super(ChannelUp, self).__init__([self.VALUE])


class ChannelDown(PICCommand):

    VALUE = 15

    def __init__(self):
        super(ChannelDown, self).__init__([self.VALUE])


class Macro(PICCommand):

    VALUE = 18

    def __init__(self, number):
        super(Macro, self).__init__([self.VALUE, number])


class Info(PICCommand):

    VALUE = 19

    def __init__(self):
        super(Info, self).__init__([self.VALUE])


class Digit(PICCommand):

    BASE_VALUE = 20

    def __init__(self, digit):
        super(Digit, self).__init__([self.BASE_VALUE + digit])
