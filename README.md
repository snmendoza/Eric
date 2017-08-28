Eric
====

Eric: Room Integrated Controller

Requirements
------------

* Kivy 1.10.0. [See installation instructions](https://kivy.org/docs/installation/installation.html).
* Pip packages listed on requirements.txt
* ALSA development headers

Configuration
-------------

This app needs a `config.json` file. Use `config.json.example` for reference.
Up to 6 lights are supported.

Installation on Raspberry Pi
----------------------------

These instructions are for installing Eric on a Raspberry Pi.
The chosen OS is Raspbian Jessie Lite.
Official touch display will be assumed as the input device.

* Download and install Raspbian Jessie Lite. [Download page and instructions](https://www.raspberrypi.org/downloads/raspbian/).
* (Optional) Change keyboard layout.
```
$ sudo dpkg-reconfigure keyboard-configuration
$ sudo reboot
```
* (Optional) [Set up WiFi](https://www.raspberrypi.org/documentation/configuration/wireless/wireless-cli.md).
* (Optional) [Use a static IP address](https://www.modmypi.com/blog/how-to-give-your-raspberry-pi-a-static-ip-address-update).
* (Optional) [Enable SSH](https://www.raspberrypi.org/documentation/remote-access/ssh/).
* Update package index and install dependencies.
```
$ sudo apt-get update; sudo apt-get install git python-setuptools
$ sudo easy_install -U pip
```
* Clone app repo.
```
$ git clone https://github.com/stupidusername/Eric.git ~/eric
```
* Install Kivy >= 1.10. [Instructions for Raspberry Pi](https://kivy.org/docs/installation/installation-rpi.html).
* Install app requirements.
```
$ sudo pip install -r ~/eric/requirements.txt
```
* Configure Kivy to use the touch display as user input. [See installation guide of Kivy](https://kivy.org/docs/installation/installation-rpi.html#using-official-rpi-touch-display).
* Configure app by editing ~/eric/config.json. When running the app on a Raspberry Pi the property "audio_mixer" should take the value "PCM".
```
$ cp ~/eric/config.json.example ~/eric/config.json
$ nano config.json
```
* Do a test run.
```
$ python ~/eric/main.py
```
* Enable autologin for pi user.
```
$ sudo nano /etc/systemd/system/getty.target.wants/getty@tty1.service
```
change
```
ExecStart=-/sbin/agetty --noclear %I $TERM
```
to
```
ExecStart=-/sbin/agetty -a pi %I $TERM
```
* Edit .bashrc to execute Eric after login.
```
$ nano ~/.bashrc
```
add these lines at the end of the file
```
sudo su -c "chmod a+w /sys/class/backlight/rpi_backlight/bl_power /sys/class/backlight/rpi_backlight/brightness"
sh ~/eric/loop.sh
```
