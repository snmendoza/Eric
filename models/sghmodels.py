from commands.basecommands import SGHCommand
from money import Money
import datetime


class Status(object):

    def __init__(self, command):
        self.app_can_update = bool(command[len(SGHCommand.START)])


class AudioMsg(object):

    def __init__(self, command):
        offset = len(SGHCommand.START)
        self.key = command[offset]
        self.room_number = command[offset + 1]
        self.suffix = ['M', 'T', 'N'][command[offset + 2]]


class Info(object):

    def __init__(self, command):
        offset = len(SGHCommand.START)
        self.datetime = datetime.datetime.strptime(
            command[offset:offset + 10], '%d%m%y%H%M')
        self.service_open = bool(command[offset + 10])
        self.shift_start_time = datetime.datetime.strptime(
            command[offset + 11:offset + 15], '%H%M').time()
        self.shift_end_time = datetime.datetime.strptime(
            command[offset + 15:offset + 19], '%H%M').time()
        self.shift_alarm_time = datetime.datetime.strptime(
            command[offset + 19:offset + 23], '%H%M').time()
        self.bill_lodging = Money(command[offset + 23:offset + 29], 'ARS')
        self.bill_surcharge = Money(command[offset + 29:offset + 35], 'ARS')
        self.bill_bar = Money(command[offset + 35:offset + 41], 'ARS')
        self.bill_bonus = Money(command[offset + 41:offset + 47], 'ARS')
        self.bill_discount = Money(command[offset + 47:offset + 53], 'ARS')
        self.bill_paid = Money(command[offset + 53:offset + 59], 'ARS')
        self.bill_total = Money(command[offset + 59:offset + 65], 'ARS')
        self.special_offer = command[offset + 65:offset + 95]
