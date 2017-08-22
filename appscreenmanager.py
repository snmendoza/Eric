class RPIScreenManager(object):

    def set_power(self, on):
        value = '0' if on else '1'
        with open('/sys/class/backlight/rpi_backlight/bl_power', 'w') as f:
            f.write(value)

    def set_brightness(self, brightness):
        # brighntess must be an integer between 0 and 100
        brightness = max(0, min(100, brightness))
        # for RPI 0 is min and 255 is max
        brightness = 255 * brightness / 100
        with open('/sys/class/backlight/rpi_backlight/brightness', 'w') as f:
            f.write(str(brightness))


ScreenManager = RPIScreenManager()
