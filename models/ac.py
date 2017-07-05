# -*- coding: utf-8 -*-

from commands.basecommands import PICCommand
from flufl.enum import Enum
from models.light import Light


class AC(object):

    class Status(Enum):

        off = 0
        turning_on = 1
        on = 2
        turning_off = 3

    TEMPS = [19, 21, 23, 25, 27, 29]

    def __init__(self):
        # Initialize with default status and temp
        self.set_status(0)
        self.set_temp(2)

    def set_status(self, status_code):
        self.status = self.Status[status_code]
        self.status_label = {
            self.Status.off: 'Apagado',
            self.Status.turning_on: 'Encendiéndose',
            self.Status.turning_off: 'Apagandose',
            self.Status.on: 'Encendido'
        }[self.status]

    def set_temp(self, temp_code):
        self.temp_code = temp_code
        self.temp = self.TEMPS[temp_code]
        if self.temp <= 21:
            self.mode = 'Frio'
        elif self.temp <= 25:
            self.mode = 'Auto'
        else:
            self.mode = 'Calor'

    def temp_down(self):
        if self.temp_code > 0:
            self.set_temp(self.temp_code - 1)

    def temp_up(self):
        if self.temp_code < len(self.TEMPS) - 1:
            self.set_temp(self.temp_code + 1)

    def update_from_command(self, command):
        offset = len(PICCommand.START) + Light.MAX_LIGHTS
        self.set_status(command[offset])
        self.set_temp(command[offset + 1])
