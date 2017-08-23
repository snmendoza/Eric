class RPIScreenManager(object):

    CONFIG_FOLDER = '/sys/class/backlight/rpi_backlight/'

    def set_power(self, on):
        value = '0' if on else '1'
        try:
            with open(self.CONFIG_FOLDER + 'bl_power', 'w') as f:
                f.write(value)
        except IOError:
            pass

    def set_brightness(self, brightness):
        # brighntess must be an integer between 0 and 100
        brightness = max(0, min(100, brightness))
        # for RPI 0 is min and 255 is max
        brightness = 255 * brightness / 100
        try:
            with open(self.CONFIG_FOLDER + 'brightness', 'w') as f:
                f.write(str(brightness))
        except IOError:
            pass


ScreenManager = RPIScreenManager()
